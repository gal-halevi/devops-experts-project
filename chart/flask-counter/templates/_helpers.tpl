{{- define "flask-counter.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "flask-counter.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name -}}
{{- end -}}

{{- define "flask-counter.labels" -}}
{{- range $key, $val := .Values.labels -}}
{{ $key }}: {{ $val | quote }}
{{- end -}}
{{- end -}}