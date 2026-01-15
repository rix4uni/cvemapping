package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
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
	TotalCount        int                 `json:"total_count"`
	IncompleteResults bool                `json:"incomplete_results"`
	Items             []*GitHubRepository `json:"items"`
}

type Owner struct {
	Login   string `json:"login"`
	HTMLURL string `json:"html_url"`
}

type GitHubRepository struct {
	ID              int64     `json:"id"`
	Name            string    `json:"name"`
	FullName        string    `json:"full_name"`
	HTMLURL         string    `json:"html_url"`
	Description     string    `json:"description"`
	StargazersCount int       `json:"stargazers_count"`
	ForksCount      int       `json:"forks_count"`
	Language        string    `json:"language"`
	UpdatedAt       string    `json:"updated_at"`
	PushedAt        string    `json:"pushed_at"`
	CreatedAt       string    `json:"created_at"`
	Topics          []string  `json:"topics"`
	Owner           Owner     `json:"owner"`
	CloneURL        string    `json:"clone_url"`
}

type CVERepository struct {
	ID              int64    `json:"id"`
	Name            string   `json:"name"`
	FullName        string   `json:"full_name"`
	HTMLURL         string   `json:"html_url"`
	Description     string   `json:"description"`
	StargazersCount int      `json:"stargazers_count"`
	ForksCount      int      `json:"forks_count"`
	Language        string   `json:"language"`
	UpdatedAt       string   `json:"updated_at"`
	PushedAt        string   `json:"pushed_at"`
	CreatedAt       string   `json:"created_at"`
	Topics          []string `json:"topics"`
	Owner           Owner    `json:"owner"`
	CloneURL        string   `json:"clone_url"`
}

type CVEEntry struct {
	CVEID        string           `json:"cve_id"`
	Repositories []CVERepository  `json:"repositories"`
}

type CVEYearData struct {
	Year  int         `json:"year"`
	CVEs  []CVEEntry  `json:"cves"`
}

func main() {
	// Get command-line arguments
	token := flag.String("github-token", "", "GitHub Token for authentication")
	page := flag.String("page", "1", "Page number to fetch, or 'all'")
	year := flag.String("year", "", "Year to search for CVEs (e.g., 2024, 2020)")
	exportJSON := flag.Bool("export-json", false, "Export data to JSON files instead of cloning")
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

	var allRepos []*GitHubRepository
	var totalCount int
	
	if *page == "all" && *year != "" {
		// First, try standard search to check total_count
		yearInt, err := strconv.Atoi(*year)
		if err != nil {
			log.Fatalf("Invalid year: %v", err)
		}
		
		// Fetch first page to check total_count
		repos, err := fetchGitHubRepositories(input, *token, 1)
		if err != nil {
			log.Fatalf("Error fetching repositories: %v", err)
		}
		
		totalCount = repos.TotalCount
		if repos.IncompleteResults {
			log.Printf("Warning: GitHub API returned incomplete results (total_count: %d)", totalCount)
		}
		log.Printf("GitHub API reports %d total results", totalCount)
		
		// Only use monthly search strategy if total_count > 1000
		if totalCount > 1000 {
			log.Printf("Total count exceeds 1000, using monthly search strategy for year %d to work around GitHub's 1000-result limit", yearInt)
			var allMonthlyRepos []*GitHubRepository
			var totalMonthlyCount int
			
			// Add first page results
			allMonthlyRepos = append(allMonthlyRepos, repos.Items...)
			
			// Loop through all 12 months
			for month := 1; month <= 12; month++ {
				monthRepos, monthCount, err := fetchRepositoriesForMonth(input, *token, yearInt, month)
				if err != nil {
					log.Printf("Error fetching repositories for month %d: %v", month, err)
					continue
				}
				
				allMonthlyRepos = append(allMonthlyRepos, monthRepos...)
				totalMonthlyCount += monthCount
				
				// Sleep between months to avoid rate limits
				if month < 12 {
					time.Sleep(2 * time.Second)
				}
			}
			
			// Deduplicate repositories by ID (some repos might appear in multiple months)
			allRepos = deduplicateRepositories(allMonthlyRepos)
			log.Printf("Deduplicated: %d unique repositories from %d total fetched across all months", len(allRepos), len(allMonthlyRepos))
			log.Printf("Finished fetching: %d unique repositories (estimated %d total across all months)", len(allRepos), totalMonthlyCount)
		} else {
			// Use standard pagination (total_count <= 1000)
			log.Printf("Total count is %d (<= 1000), using standard pagination", totalCount)
			allRepos = append(allRepos, repos.Items...)
			pageNum := 2
			
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
				log.Printf("Fetched page %d: %d repositories (total fetched: %d/%d)", pageNum, len(repos.Items), len(allRepos), totalCount)

				// Stop if no more items or we've reached the GitHub API limit (1000 results)
				if len(repos.Items) == 0 || len(allRepos) >= 1000 {
					if len(allRepos) >= 1000 && totalCount > 1000 {
						log.Printf("Reached GitHub API limit of 1000 results (total available: %d)", totalCount)
					}
					break
				}

				// Stop if we've fetched all available results
				if len(allRepos) >= totalCount {
					break
				}

				pageNum++

				// Sleep to avoid hitting the rate limit
				time.Sleep(3 * time.Second)
			}
			
			log.Printf("Finished fetching: %d repositories from %d total available", len(allRepos), totalCount)
		}
	} else {
		// Use standard pagination (for single page requests or when year is not specified)
		pageNum := 1
		if *page != "all" {
			pageNum, _ = strconv.Atoi(*page)
		}
		
		for {
			repos, err := fetchGitHubRepositories(input, *token, pageNum)
			if err != nil {
				if strings.Contains(err.Error(), "422") {
					log.Println("Reached the limit of 1000 results for the query.")
					break
				}
				log.Fatalf("Error fetching repositories: %v", err)
			}

			// Capture total_count and incomplete_results from first page
			if pageNum == 1 {
				totalCount = repos.TotalCount
				if repos.IncompleteResults {
					log.Printf("Warning: GitHub API returned incomplete results (total_count: %d)", totalCount)
				}
				log.Printf("GitHub API reports %d total results", totalCount)
			}

			allRepos = append(allRepos, repos.Items...)
			log.Printf("Fetched page %d: %d repositories (total fetched: %d/%d)", pageNum, len(repos.Items), len(allRepos), totalCount)

			// Check if we've fetched all available results
			if *page != "all" {
				break
			}

			// Stop if no more items or we've reached the GitHub API limit (1000 results)
			if len(repos.Items) == 0 || len(allRepos) >= 1000 {
				if len(allRepos) >= 1000 && totalCount > 1000 {
					log.Printf("Reached GitHub API limit of 1000 results (total available: %d)", totalCount)
				}
				break
			}

			// Stop if we've fetched all available results
			if len(allRepos) >= totalCount {
				break
			}

			pageNum++

			// Sleep to avoid hitting the rate limit
			time.Sleep(3 * time.Second)
		}
		
		log.Printf("Finished fetching: %d repositories from %d total available", len(allRepos), totalCount)
	}

	if *exportJSON {
		// Export to JSON
		err := exportToJSON(allRepos, *year)
		if err != nil {
			log.Fatalf("Error exporting to JSON: %v", err)
		}
	} else {
		// Clone the repositories (existing behavior)
		reposToClone := processRepos(allRepos, *year)

		// Clone the repositories
		for _, repo := range reposToClone {
			err := cloneRepo(repo.CloneURL, repo.CVEName, repo.StargazersCount, *year)
			if err != nil {
				log.Printf("Error cloning repo %s: %v", repo.CloneURL, err)
			}
		}
	}
}

// Function to get the last day of a month (handles leap years)
func getLastDayOfMonth(year, month int) int {
	// Create a date for the first day of the next month, then subtract one day
	lastDay := time.Date(year, time.Month(month+1), 0, 0, 0, 0, 0, time.UTC)
	return lastDay.Day()
}

// Function to fetch all repositories for a given month using date range
func fetchRepositoriesForMonth(baseQuery string, token string, year int, month int) ([]*GitHubRepository, int, error) {
	// Get the last day of the month
	lastDay := getLastDayOfMonth(year, month)
	
	// Format dates as YYYY-MM-DD
	startDate := fmt.Sprintf("%04d-%02d-01", year, month)
	endDate := fmt.Sprintf("%04d-%02d-%02d", year, month, lastDay)
	
	// Build query with date range: baseQuery created:startDate..endDate
	dateQuery := fmt.Sprintf("%s created:%s..%s", baseQuery, startDate, endDate)
	
	var allRepos []*GitHubRepository
	var totalCount int
	pageNum := 1
	
	for {
		repos, err := fetchGitHubRepositories(dateQuery, token, pageNum)
		if err != nil {
			if strings.Contains(err.Error(), "422") {
				log.Printf("Month %d: Reached the limit of 1000 results for this month", month)
				break
			}
			return nil, 0, err
		}
		
		// Capture total_count from first page
		if pageNum == 1 {
			totalCount = repos.TotalCount
			log.Printf("Month %d (%s to %s): GitHub API reports %d total results", month, startDate, endDate, totalCount)
		}
		
		allRepos = append(allRepos, repos.Items...)
		
		// Stop if no more items or we've reached the GitHub API limit (1000 results)
		if len(repos.Items) == 0 || len(allRepos) >= 1000 {
			if len(allRepos) >= 1000 && totalCount > 1000 {
				log.Printf("Month %d: Reached GitHub API limit of 1000 results (total available: %d)", month, totalCount)
			}
			break
		}
		
		// Stop if we've fetched all available results
		if len(allRepos) >= totalCount {
			break
		}
		
		pageNum++
		time.Sleep(2 * time.Second) // Sleep between pages
	}
	
	log.Printf("Month %d: Fetched %d repositories from %d total available", month, len(allRepos), totalCount)
	return allRepos, totalCount, nil
}

// Function to fetch repositories directly from GitHub API
func fetchGitHubRepositories(query, token string, page int) (*GitHubSearchResponse, error) {
	client := &http.Client{}
	
	// URL encode the query string
	encodedQuery := url.QueryEscape(query)
	
	// Add per_page=100 to maximize results per page (max is 100)
	apiURL := fmt.Sprintf(`https://api.github.com/search/repositories?q=%s&sort=updated&order=desc&page=%d&per_page=100`, encodedQuery, page)

	req, err := http.NewRequest("GET", apiURL, nil)
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

// Deduplicate repositories by ID
func deduplicateRepositories(repos []*GitHubRepository) []*GitHubRepository {
	seen := make(map[int64]bool)
	deduplicated := []*GitHubRepository{}

	for _, repo := range repos {
		if !seen[repo.ID] {
			seen[repo.ID] = true
			deduplicated = append(deduplicated, repo)
		}
	}

	return deduplicated
}

// Convert GitHubRepository to CVERepository
func toCVERepository(repo *GitHubRepository) CVERepository {
	return CVERepository{
		ID:              repo.ID,
		Name:            repo.Name,
		FullName:        repo.FullName,
		HTMLURL:         repo.HTMLURL,
		Description:     repo.Description,
		StargazersCount: repo.StargazersCount,
		ForksCount:      repo.ForksCount,
		Language:        repo.Language,
		UpdatedAt:       repo.UpdatedAt,
		PushedAt:        repo.PushedAt,
		CreatedAt:       repo.CreatedAt,
		Topics:          repo.Topics,
		Owner:           repo.Owner,
		CloneURL:        repo.CloneURL,
	}
}

// Export repositories to JSON files organized by year
func exportToJSON(repos []*GitHubRepository, year string) error {
	// Create data directory if it doesn't exist
	dataDir := "data"
	if err := os.MkdirAll(dataDir, 0755); err != nil {
		return fmt.Errorf("failed to create data directory: %w", err)
	}

	// Group repositories by CVE ID
	cveMap := make(map[string][]CVERepository)
	cveRegex := regexp.MustCompile(fmt.Sprintf(`(?i)cve-%s-\d+`, year))
	catchAllKey := fmt.Sprintf("OTHER-%s", year)

	for _, repo := range repos {
		// Find CVE in the repository name, full name, description, or topics
		searchText := repo.Name + " " + repo.FullName + " " + repo.Description
		for _, topic := range repo.Topics {
			searchText += " " + topic
		}

		matches := cveRegex.FindAllString(searchText, -1)
		cveRepo := toCVERepository(repo)

		if len(matches) == 0 {
			// Repository doesn't match any CVE pattern, add to catch-all
			cveMap[catchAllKey] = append(cveMap[catchAllKey], cveRepo)
		} else {
			uniqueMatches := uniqueStrings(matches)
			// Add repository to each matching CVE
			for _, match := range uniqueMatches {
				cveName := strings.ToUpper(match)
				cveMap[cveName] = append(cveMap[cveName], cveRepo)
			}
		}
	}

	// Convert map to slice of CVEEntry
	var cveEntries []CVEEntry
	for cveID, repositories := range cveMap {
		// Deduplicate repositories within each CVE entry by ID
		seenIDs := make(map[int64]bool)
		uniqueRepos := []CVERepository{}
		for _, repo := range repositories {
			if !seenIDs[repo.ID] {
				seenIDs[repo.ID] = true
				uniqueRepos = append(uniqueRepos, repo)
			}
		}

		// Sort repositories by stargazers count (descending)
		sortedRepos := uniqueRepos
		for i := 0; i < len(sortedRepos)-1; i++ {
			for j := i + 1; j < len(sortedRepos); j++ {
				if sortedRepos[i].StargazersCount < sortedRepos[j].StargazersCount {
					sortedRepos[i], sortedRepos[j] = sortedRepos[j], sortedRepos[i]
				}
			}
		}

		cveEntries = append(cveEntries, CVEEntry{
			CVEID:        cveID,
			Repositories: sortedRepos,
		})
	}

	// Sort CVEs by ID
	for i := 0; i < len(cveEntries)-1; i++ {
		for j := i + 1; j < len(cveEntries); j++ {
			if cveEntries[i].CVEID > cveEntries[j].CVEID {
				cveEntries[i], cveEntries[j] = cveEntries[j], cveEntries[i]
			}
		}
	}

	// Create year data structure
	yearInt, _ := strconv.Atoi(year)
	yearData := CVEYearData{
		Year: yearInt,
		CVEs: cveEntries,
	}

	// Write JSON file
	jsonFile := fmt.Sprintf("%s/%s.json", dataDir, year)
	jsonData, err := json.MarshalIndent(yearData, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal JSON: %w", err)
	}

	err = ioutil.WriteFile(jsonFile, jsonData, 0644)
	if err != nil {
		return fmt.Errorf("failed to write JSON file: %w", err)
	}

	log.Printf("Exported %d CVEs to %s", len(cveEntries), jsonFile)
	return nil
}