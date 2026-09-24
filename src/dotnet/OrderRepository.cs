using System.Data.SqlClient;

namespace Lab.Data
{
    public class OrderRepository
    {
        private readonly SqlConnection _connection;

        public OrderRepository(SqlConnection connection)
        {
            _connection = connection;
        }

        public SqlDataReader FindOrdersByCustomer(string customerId)
        {
            var command = new SqlCommand("SELECT Id, Total FROM Orders WHERE CustomerId = '" + customerId + "'", _connection);
            return command.ExecuteReader();
        }

        public SqlDataReader SearchOrders(string term)
        {
            var command = new SqlCommand("SELECT Id FROM Orders WHERE Note LIKE '%" + term + "%'", _connection);
            return command.ExecuteReader();
        }

        public SqlDataReader FindOrdersByStatus(string status)
        {
            var command = new SqlCommand("SELECT Id FROM Orders WHERE Status = '" + status + "'", _connection);
            return command.ExecuteReader();
        }
    }
}
