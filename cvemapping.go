package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"time"
	"path/filepath"
)

type RepoDetails struct {
	CloneURL        string
	Description     string
	StargazersCount int
	CVEName         string
}

type GitHubSearchResponse struct {
	Items []*GitHubRepository `json:"items"`
}

type GitHubRepository struct {
	CloneURL        string `json:"clone_url"`
	Description     string `json:"description"`
	StargazersCount int    `json:"stargazers_count"`
}

func main() {
	// Get command-line arguments
	token := flag.String("github-token", "", "GitHub Token for authentication")
	page := flag.String("page", "1", "Page number to fetch, or 'all'")
	year := flag.String("year", "", "Year to search for CVEs (e.g., 2024, 2020)")
	flag.Parse()

	// Disable log timestamps
	log.SetFlags(0)

	if *token == "" {
		log.Fatal("GitHub token is required")
	}

	// Read input from stdin (for "CVE-<year>-*" pattern)
	reader := bufio.NewReader(os.Stdin)
	input, err := reader.ReadString('\n')
	if err != nil {
		log.Fatalf("Error reading input: %v", err)
	}
	input = strings.TrimSpace(input) // Remove newline character

	pageNum := 1
	if *page != "all" {
		pageNum, _ = strconv.Atoi(*page)
	}

	// Fetch repositories using GitHub API directly
	var allRepos []*GitHubRepository
	for {
		repos, err := fetchGitHubRepositories(input, *token, pageNum)
		if err != nil {
			if strings.Contains(err.Error(), "422") {
				log.Println("Reached the limit of 1000 results for the query.")
				break
			}
			log.Fatalf("Error fetching repositories: %v", err)
		}

		allRepos = append(allRepos, repos.Items...)

		if *page != "all" || len(repos.Items) == 0 {
			break
		}
		pageNum++

		// Sleep for 1 second to avoid hitting the rate limit
		time.Sleep(3 * time.Second)
	}

	reposToClone := processRepos(allRepos, *year)

	// Clone the repositories
	for _, repo := range reposToClone {
		err := cloneRepo(repo.CloneURL, repo.CVEName, repo.StargazersCount, *year)
		if err != nil {
			log.Printf("Error cloning repo %s: %v", repo.CloneURL, err)
		}
	}
}

// Function to fetch repositories directly from GitHub API
func fetchGitHubRepositories(query, token string, page int) (*GitHubSearchResponse, error) {
	client := &http.Client{}
	url := fmt.Sprintf(`https://api.github.com/search/repositories?q=%s&sort=updated&order=desc&page=%d`, query, page)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "token "+token)

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := ioutil.ReadAll(resp.Body)
		return nil, fmt.Errorf("failed to fetch repositories, status: %d, response: %s", resp.StatusCode, string(body))
	}

	var searchResponse GitHubSearchResponse
	if err := json.NewDecoder(resp.Body).Decode(&searchResponse); err != nil {
		return nil, err
	}

	return &searchResponse, nil
}

// Process repositories based on filtering rules
func processRepos(repos []*GitHubRepository, year string) []RepoDetails {
	var reposToClone []RepoDetails
	cveRegex := regexp.MustCompile(fmt.Sprintf(`(?i)cve-%s-\d+`, year))
	cveMap := make(map[string]RepoDetails)

	for _, repo := range repos {
		cloneURL := repo.CloneURL
		description := repo.Description
		stargazersCount := repo.StargazersCount

		// Find CVE in the clone URL or description
		matches := cveRegex.FindAllString(cloneURL+description, -1)
		if len(matches) == 0 {
			continue
		}

		// Remove duplicate CVE entries from matches
		uniqueMatches := uniqueStrings(matches)

		// Skip repos with more than one unique CVE
		if len(uniqueMatches) > 1 {
			log.Printf("[SKIPPING] [%d] %s", stargazersCount, cloneURL)
			continue
		}

		cveName := strings.ToUpper(uniqueMatches[0])

		// Clone the repo with the highest stargazers if multiple repos for the same CVE
		if existingRepo, exists := cveMap[cveName]; exists {
			if stargazersCount > existingRepo.StargazersCount {
				log.Printf("[SKIPPING DUPLICATE] [%d] %s (Duplicate of %s)", stargazersCount, cloneURL, existingRepo.CloneURL)
				cveMap[cveName] = RepoDetails{CloneURL: cloneURL, Description: description, StargazersCount: stargazersCount, CVEName: cveName}
			} else {
				log.Printf("[SKIPPING] [%d] %s (Already cloned: %s)", stargazersCount, cloneURL, existingRepo.CloneURL)
			}
		} else {
			cveMap[cveName] = RepoDetails{CloneURL: cloneURL, Description: description, StargazersCount: stargazersCount, CVEName: cveName}
		}
	}

	// Convert the map to a slice
	for _, repo := range cveMap {
		reposToClone = append(reposToClone, repo)
	}

	return reposToClone
}

// Function to clone the repository with custom output
func cloneRepo(cloneURL string, cveName string, stargazersCount int, year string) error {
	cloneDir := fmt.Sprintf("%s/%s", year, cveName)
	if _, err := os.Stat(cloneDir); !os.IsNotExist(err) {
		// Directory already exists
		fmt.Printf("[ALREADY EXISTS] [%d] %s into %s\n", stargazersCount, cloneURL, cloneDir)
		return nil
	}

	// Execute the git clone command
	cmd := exec.Command("git", "clone", "--depth", "1", cloneURL, cloneDir)
	err := cmd.Run()

	if err != nil {
		return fmt.Errorf("failed to clone repository: %w", err)
	}

	fmt.Printf("[CLONED] [%d] %s into %s\n", stargazersCount, cloneURL, cloneDir)

	// List of items to remove
	itemsToRemove := []string{
		".git",
		".github",
		".gitignore",
		".gitattributes",
		"LICENSE",
	}

	// Remove the .git directory and other specified files/directories
	for _, item := range itemsToRemove {
		itemPath := filepath.Join(cloneDir, item)
		if err := os.RemoveAll(itemPath); err != nil {
			return fmt.Errorf("failed to remove %s: %w", item, err)
		}
		fmt.Printf("[REMOVED %s] from %s\n", item, cloneDir)
	}

	// Check directory size and file count
	dirSize, fileCount, err := getDirSizeAndFileCount(cloneDir)
	if err != nil {
		return fmt.Errorf("failed to check directory size or file count: %w", err)
	}

	// If directory size > 1MB or file count > 5, delete the directory
	if dirSize > 1*1024*1024 || fileCount > 5 {
		if err := os.RemoveAll(cloneDir); err != nil {
			return fmt.Errorf("failed to delete directory: %w", err)
		}
		fmt.Printf("[DELETED] %s because size was %d bytes or had %d files\n", cloneDir, dirSize, fileCount)
	} else {
		fmt.Printf("[KEPT] %s with size %d bytes and %d files\n", cloneDir, dirSize, fileCount)
	}

	return nil
}

// Helper function to calculate directory size and count files
func getDirSizeAndFileCount(path string) (int64, int, error) {
	var totalSize int64
	var fileCount int

	err := filepath.Walk(path, func(_ string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		// Add file size
		if !info.IsDir() {
			totalSize += info.Size()
			fileCount++
		}
		return nil
	})

	if err != nil {
		return 0, 0, err
	}

	return totalSize, fileCount, nil
}

// Helper function to remove duplicate strings from a slice
func uniqueStrings(input []string) []string {
	keys := make(map[string]bool)
	list := []string{}

	for _, entry := range input {
		if _, exists := keys[entry]; !exists {
			keys[entry] = true
			list = append(list, entry)
		}
	}

	return list
}