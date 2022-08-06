package main

import "fmt"

const (
	FOO = iota
	BAR = iota
	BAZ = iota
)

func main() {
	fmt.Printf("FOO = %d\n", FOO)
	fmt.Printf("BAR = %d\n", BAR)
	fmt.Printf("BAZ = %d\n", BAZ)
}
