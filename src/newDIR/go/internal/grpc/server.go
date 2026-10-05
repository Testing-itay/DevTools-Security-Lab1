package grpc

import (
	"net"

	"google.golang.org/grpc"
)

// Server wraps a gRPC server.
type Server struct {
	grpcServer *grpc.Server
	listener   net.Listener
}

// NewServer creates and configures a gRPC server.
func NewServer(addr string) (*Server, error) {
	lis, err := net.Listen("tcp", addr)
	if err != nil {
		return nil, err
	}
	grpcServer := grpc.NewServer()
	return &Server{
		grpcServer: grpcServer,
		listener:   lis,
	}, nil
}

// RegisterService registers a service with the gRPC server.
func (s *Server) RegisterService(desc *grpc.ServiceDesc, impl interface{}) {
	s.grpcServer.RegisterService(desc, impl)
}

// Serve starts the gRPC server.
func (s *Server) Serve() error {
	return s.grpcServer.Serve(s.listener)
}

// Stop gracefully stops the server.
func (s *Server) Stop() {
	s.grpcServer.GracefulStop()
}
