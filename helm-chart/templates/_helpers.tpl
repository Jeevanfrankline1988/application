{{- define "pygame.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "pygame.fullname" -}}
{{- printf "%s-%s" (include "pygame.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
