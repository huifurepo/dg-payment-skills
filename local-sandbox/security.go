package main

import (
	"context"
	"fmt"
	"net"
	"net/url"
	"strings"
	"time"
)

type PinnedTarget struct {
	URL  *url.URL
	Host string
	Port string
	IP   net.IP
}

func (target *PinnedTarget) String() string {
	if target == nil || target.URL == nil {
		return ""
	}
	return target.URL.String()
}

func (a *App) addNotifyAllow(raw string) error {
	u, err := parseNotifyURL(raw)
	if err != nil {
		return err
	}
	a.mu.Lock()
	defer a.mu.Unlock()
	a.notifyAllowlist[u.String()] = struct{}{}
	return nil
}

func (a *App) validateNotifyTarget(raw string) (*PinnedTarget, error) {
	allowlist := a.notifyAllowlistSnapshot()
	u, err := validateNotifyTarget(raw, allowlist)
	if err != nil {
		a.recordSecurityFinding("notify_target_blocked", raw, err.Error())
		return nil, err
	}
	return u, nil
}

func (a *App) notifyAllowlistSnapshot() map[string]struct{} {
	a.mu.Lock()
	defer a.mu.Unlock()
	out := make(map[string]struct{}, len(a.notifyAllowlist))
	for key := range a.notifyAllowlist {
		out[key] = struct{}{}
	}
	return out
}

func (a *App) recordSecurityFinding(kind, rawTarget, reason string) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.securityFindings = append(a.securityFindings, SecurityFinding{
		Time:           time.Now().UTC().Format(time.RFC3339Nano),
		Type:           kind,
		Severity:       "high",
		Target:         rawTarget,
		TargetRedacted: redactTarget(rawTarget),
		Reason:         sanitizePlainLogText(reason),
	})
}

func validateReplayTarget(raw string) error {
	_, err := validateNotifyTarget(raw, nil)
	return err
}

func validateNotifyTarget(raw string, allowlist map[string]struct{}) (*PinnedTarget, error) {
	u, err := parseNotifyURL(raw)
	if err != nil {
		return nil, err
	}
	normalized := u.String()
	host := strings.ToLower(u.Hostname())
	if host == "" {
		return nil, securityError("notify target missing host")
	}
	port := notifyPort(u)
	if host == "localhost" {
		return &PinnedTarget{URL: u, Host: host, Port: port, IP: net.ParseIP("127.0.0.1")}, nil
	}
	ip := net.ParseIP(host)
	if ip != nil {
		if ip.IsLoopback() {
			return &PinnedTarget{URL: u, Host: host, Port: port, IP: ip}, nil
		}
		if reason := blockedIPReason(ip); reason != "" {
			return nil, securityError(reason)
		}
		if _, ok := allowlist[normalized]; !ok {
			return nil, securityError("external notify target requires --notify-allow exact URL")
		}
		return &PinnedTarget{URL: u, Host: host, Port: port, IP: ip}, nil
	}
	if _, ok := allowlist[normalized]; !ok {
		return nil, securityError("external notify target requires --notify-allow exact URL")
	}
	ips, err := resolveNotifyHost(host)
	if err != nil {
		return nil, securityError("notify target DNS resolution failed: " + err.Error())
	}
	for _, ip := range ips {
		if ip.IsLoopback() {
			return &PinnedTarget{URL: u, Host: host, Port: port, IP: ip}, nil
		}
		if reason := blockedIPReason(ip); reason != "" {
			return nil, securityError("notify target DNS resolved to blocked address: " + reason)
		}
		return &PinnedTarget{URL: u, Host: host, Port: port, IP: ip}, nil
	}
	return nil, securityError("notify target DNS resolution returned no usable address")
}

func parseNotifyURL(raw string) (*url.URL, error) {
	if strings.TrimSpace(raw) == "" {
		return nil, usageError("notify target is required")
	}
	u, err := url.Parse(strings.TrimSpace(raw))
	if err != nil {
		return nil, err
	}
	if u.Scheme != "http" && u.Scheme != "https" {
		return nil, securityError("notify target must be http or https")
	}
	if u.User != nil {
		return nil, securityError("notify target must not include userinfo")
	}
	if u.Hostname() == "" {
		return nil, securityError("notify target missing host")
	}
	// notify_url 文档建议不带 query 参数（shared-async-notify.md:14）。
	// 沙箱不强制拒绝，避免阻断接入方带 query 的真实回调演练；真实环境口径以文档为准。
	return u, nil
}

func resolveNotifyHost(host string) ([]net.IP, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	addrs, err := net.DefaultResolver.LookupIPAddr(ctx, host)
	if err != nil {
		return nil, err
	}
	if len(addrs) == 0 {
		return nil, fmt.Errorf("no addresses")
	}
	ips := make([]net.IP, 0, len(addrs))
	for _, addr := range addrs {
		ips = append(ips, addr.IP)
	}
	return ips, nil
}

func notifyPort(u *url.URL) string {
	if port := u.Port(); port != "" {
		return port
	}
	if u.Scheme == "https" {
		return "443"
	}
	return "80"
}

func blockedIPReason(ip net.IP) string {
	if ip.Equal(net.ParseIP("169.254.169.254")) {
		return "metadata IP is not allowed"
	}
	if ip.IsUnspecified() {
		return "unspecified IP is not allowed"
	}
	if ip.IsPrivate() {
		return "private non-loopback IP is not allowed"
	}
	if ip.IsLinkLocalUnicast() || ip.IsLinkLocalMulticast() {
		return "link-local IP is not allowed"
	}
	if ip.IsMulticast() {
		return "multicast IP is not allowed"
	}
	return ""
}

func redactTarget(raw string) string {
	u, err := url.Parse(raw)
	if err != nil {
		return raw
	}
	u.Fragment = ""
	if u.RawQuery != "" {
		u.RawQuery = "REDACTED"
	}
	return u.String()
}
