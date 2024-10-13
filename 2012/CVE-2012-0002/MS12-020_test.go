package rdp

import (
	"fmt"
	"testing"
)

func TestMS12_020(t *testing.T) {
	result := checkRDPVuln("192.168.18.143", 3389)
	fmt.Println("Result:", result)
}
