package logger

import (
	"os"

	"github.com/sirupsen/logrus"
)

// Logger wraps logrus.Logger for convenience
type Logger = logrus.Logger

// SetupLogger configures structured logging
func SetupLogger(level string, jsonOutput bool) *logrus.Logger {
	logger := logrus.New()

	// Set log level
	switch level {
	case "DEBUG":
		logger.SetLevel(logrus.DebugLevel)
	case "INFO":
		logger.SetLevel(logrus.InfoLevel)
	case "WARNING":
		logger.SetLevel(logrus.WarnLevel)
	case "ERROR":
		logger.SetLevel(logrus.ErrorLevel)
	default:
		logger.SetLevel(logrus.InfoLevel)
	}

	// Set output format
	if jsonOutput {
		logger.SetFormatter(&logrus.JSONFormatter{
			TimestampFormat: "2006-01-02T15:04:05.000Z07:00",
		})
	} else {
		logger.SetFormatter(&logrus.TextFormatter{
			FullTimestamp:   true,
			TimestampFormat: "2006-01-02T15:04:05.000Z07:00",
		})
	}

	logger.SetOutput(os.Stdout)
	return logger
}

// GetLogger returns a logger instance
func GetLogger() *logrus.Logger {
	return logrus.StandardLogger()
}
