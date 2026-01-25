module deployment-orchestrator

go 1.21

require (
	github.com/docker/docker v24.0.7+incompatible
	github.com/sirupsen/logrus v1.9.3
	github.com/spf13/cobra v1.8.0
	golang.org/x/crypto v0.17.0
	gopkg.in/yaml.v3 v3.0.1
	k8s.io/client-go v0.28.4
)
