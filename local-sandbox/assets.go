package main

import "embed"

//go:embed contracts/huifu-pay-integration-1.3.0-r4/**
var embeddedContracts embed.FS

//go:embed ui-assets/*
var embeddedUIAssets embed.FS
