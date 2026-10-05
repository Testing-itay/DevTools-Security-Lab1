package data

import (
	"context"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"github.com/devtools-engine/go-service/internal/model"
)

// MongoRepo provides MongoDB CRUD operations.
type MongoRepo struct {
	col *mongo.Collection
}

// NewMongoRepo creates a new MongoRepo.
func NewMongoRepo(col *mongo.Collection) *MongoRepo {
	return &MongoRepo{col: col}
}

// Create inserts a new agent.
func (r *MongoRepo) Create(ctx context.Context, agent *model.Agent) error {
	agent.CreatedAt = time.Now()
	_, err := r.col.InsertOne(ctx, agent)
	return err
}

// GetByID fetches an agent by ID.
func (r *MongoRepo) GetByID(ctx context.Context, id string) (*model.Agent, error) {
	var agent model.Agent
	err := r.col.FindOne(ctx, bson.M{"_id": id}).Decode(&agent)
	if err != nil {
		return nil, err
	}
	return &agent, nil
}

// List returns all agents.
func (r *MongoRepo) List(ctx context.Context) ([]model.Agent, error) {
	cur, err := r.col.Find(ctx, bson.M{}, options.Find())
	if err != nil {
		return nil, err
	}
	defer cur.Close(ctx)
	var agents []model.Agent
	return agents, cur.All(ctx, &agents)
}

// Update updates an agent.
func (r *MongoRepo) Update(ctx context.Context, agent *model.Agent) error {
	_, err := r.col.UpdateOne(ctx, bson.M{"_id": agent.ID}, bson.M{"$set": agent})
	return err
}

// Delete removes an agent by ID.
func (r *MongoRepo) Delete(ctx context.Context, id string) error {
	_, err := r.col.DeleteOne(ctx, bson.M{"_id": id})
	return err
}
