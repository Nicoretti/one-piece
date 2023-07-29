# Changelog

## [{{ .version }}] - {{ .date }}
{{ .summary }}

{{ if .added -}}
### Added
{{- end }}
{{ range .added }} - {{ .Summary }}
{{ end -}}

{{ if .changed -}}
### Changed
{{- end }}
{{ range .changed }} - {{ .Summary }}
{{ end -}}

{{ if .deprecated -}}
### Deprecated
{{- end }}
{{ range .deprecated }} - {{ .Summary }}
{{ end -}}

{{ if .removed -}}
### Removed
{{- end }}
{{ range .removed }} - {{ .Summary }}
{{ end -}}

{{ if .fixed -}}
### Fixed
{{- end }}
{{ range .fixed }} - {{ .Summary }}
{{ end -}}

{{ if .security -}}
### Security
{{- end }}
{{ range .security }} - {{ .Summary }}
{{ end }}
