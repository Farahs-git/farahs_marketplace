# Domain Guide

## Overview

This guide describes the domain objects managed by the my-workflow skill and the rules that govern them.

## Object Types

| Type | Description | Required Fields |
|------|-------------|-----------------|
| `widget` | A basic domain object | `name`, `type`, `config` |
| `widget-group` | A collection of widgets | `name`, `widgets[]` |

## Constraints

- Object names must be unique within a project
- Names must be 3-100 characters, alphanumeric with hyphens
- A widget-group must contain at least one widget
- Maximum 50 widgets per widget-group

## Statuses

| Status | Description |
|--------|-------------|
| `draft` | Object is being configured, not yet active |
| `active` | Object is live and operational |
| `archived` | Object is no longer active but preserved for reference |

## Naming Conventions

Use descriptive, lowercase-hyphenated names: `my-campaign-q1-2025`
