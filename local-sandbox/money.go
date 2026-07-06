package main

import (
	"fmt"
	"strconv"
	"strings"
)

func parseAmountFen(raw string) (int64, error) {
	value := strings.TrimSpace(raw)
	if value == "" {
		return 0, fmt.Errorf("amount is required")
	}
	if strings.HasPrefix(value, "-") {
		return 0, fmt.Errorf("amount must be positive")
	}
	parts := strings.Split(value, ".")
	if len(parts) > 2 {
		return 0, fmt.Errorf("amount must have at most one decimal point")
	}
	yuanPart := parts[0]
	if yuanPart == "" {
		yuanPart = "0"
	}
	yuan, err := strconv.ParseInt(yuanPart, 10, 64)
	if err != nil {
		return 0, fmt.Errorf("amount yuan part invalid")
	}
	// maxAmountYuan 上限远超任何现实支付额，用于防止 yuan*100 在 int64 上溢出回绕。
	const maxAmountYuan = 9_000_000_000_000_0 // 9e15 元，yuan*100 仍在 int64 正区间内
	if yuan > maxAmountYuan {
		return 0, fmt.Errorf("amount exceeds maximum supported value")
	}
	fenPart := ""
	if len(parts) == 2 {
		fenPart = parts[1]
	}
	if len(fenPart) > 2 {
		return 0, fmt.Errorf("amount supports at most two decimals")
	}
	for len(fenPart) < 2 {
		fenPart += "0"
	}
	fen := int64(0)
	if fenPart != "" {
		fen, err = strconv.ParseInt(fenPart, 10, 64)
		if err != nil {
			return 0, fmt.Errorf("amount fen part invalid")
		}
	}
	total := yuan*100 + fen
	if total <= 0 {
		return 0, fmt.Errorf("amount must be greater than zero")
	}
	return total, nil
}

func formatFen(fen int64) string {
	if fen < 0 {
		fen = 0
	}
	return fmt.Sprintf("%d.%02d", fen/100, fen%100)
}
