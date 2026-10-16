

using System.Text;
using RabbitMQ.Client;

namespace DevToolsLab.Api.Messaging;

public class RabbitMqPublisher
{
    private readonly IConnection _connection;
    private readonly IModel _channel;
    private const string ExchangeName = "devtools.exchange";

    public RabbitMqPublisher(IConnection connection)
    {
        _connection = connection;
        _channel = _connection.CreateModel();
        _channel.ExchangeDeclare(ExchangeName, ExchangeType.Topic, durable: true);
    }

    public void Publish(string routingKey, string message)
    {
        var body = Encoding.UTF8.GetBytes(message);
        var properties = _channel.CreateBasicProperties();
        properties.Persistent = true;

        _channel.BasicPublish(ExchangeName, routingKey, properties, body);
    }

    public void Publish(string routingKey, byte[] body)
    {
        var properties = _channel.CreateBasicProperties();
        properties.Persistent = true;
        _channel.BasicPublish(ExchangeName, routingKey, properties, body);
    }
}
