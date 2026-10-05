package service

import (
	"context"
	"bytes"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
)

// CloudService handles AWS S3 and DynamoDB operations.
type CloudService struct {
	s3Client   *s3.Client
	dynamoClient *dynamodb.Client
}

// NewCloudService creates a new CloudService.
func NewCloudService(s3Client *s3.Client, dynamoClient *dynamodb.Client) *CloudService {
	return &CloudService{s3Client: s3Client, dynamoClient: dynamoClient}
}

// PutObject uploads data to S3.
func (cs *CloudService) PutObject(ctx context.Context, bucket, key string, data []byte) error {
	_, err := cs.s3Client.PutObject(ctx, &s3.PutObjectInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(key),
		Body:   bytes.NewReader(data),
	})
	return err
}

// GetObject retrieves data from S3.
func (cs *CloudService) GetObject(ctx context.Context, bucket, key string) ([]byte, error) {
	out, err := cs.s3Client.GetObject(ctx, &s3.GetObjectInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(key),
	})
	if err != nil {
		return nil, err
	}
	defer out.Body.Close()
	var buf bytes.Buffer
	_, err = buf.ReadFrom(out.Body)
	return buf.Bytes(), err
}

// PutItem writes an item to DynamoDB.
func (cs *CloudService) PutItem(ctx context.Context, table, id, value string) error {
	_, err := cs.dynamoClient.PutItem(ctx, &dynamodb.PutItemInput{
		TableName: aws.String(table),
		Item: map[string]types.AttributeValue{
			"id":    &types.AttributeValueMemberS{Value: id},
			"value": &types.AttributeValueMemberS{Value: value},
		},
	})
	return err
}

// GetItem retrieves an item from DynamoDB.
func (cs *CloudService) GetItem(ctx context.Context, table, id string) (string, error) {
	out, err := cs.dynamoClient.GetItem(ctx, &dynamodb.GetItemInput{
		TableName: aws.String(table),
		Key: map[string]types.AttributeValue{
			"id": &types.AttributeValueMemberS{Value: id},
		},
	})
	if err != nil {
		return "", err
	}
	if v, ok := out.Item["value"]; ok {
		if s, ok := v.(*types.AttributeValueMemberS); ok {
			return s.Value, nil
		}
	}
	return "", nil
}
