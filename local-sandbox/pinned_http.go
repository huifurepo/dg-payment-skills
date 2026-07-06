package main

import (
	"context"
	"net"
	"net/http"
	"time"
)

func (a *App) doPinned(req *http.Request, target *PinnedTarget) (*http.Response, error) {
	timeout := 5 * time.Second
	if a.httpClient != nil && a.httpClient.Timeout > 0 {
		timeout = a.httpClient.Timeout
	}
	redirect := func(req *http.Request, via []*http.Request) error {
		return securityError("redirects are not allowed for notify delivery")
	}
	if a.httpClient != nil && a.httpClient.CheckRedirect != nil {
		redirect = a.httpClient.CheckRedirect
	}
	dialer := &net.Dialer{Timeout: timeout}
	transport := &http.Transport{
		Proxy: http.ProxyFromEnvironment,
		DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
			_, port, err := net.SplitHostPort(addr)
			if err != nil || port == "" {
				port = target.Port
			}
			return dialer.DialContext(ctx, network, net.JoinHostPort(target.IP.String(), port))
		},
		TLSHandshakeTimeout: timeout,
		// 通知投递目标每次可能不同且低频，禁用 keep-alive 避免空闲连接累积。
		DisableKeepAlives: true,
	}
	client := &http.Client{Timeout: timeout, CheckRedirect: redirect, Transport: transport}
	return client.Do(req)
}
