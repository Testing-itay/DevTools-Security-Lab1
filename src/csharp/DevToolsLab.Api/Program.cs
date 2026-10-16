

using DevToolsLab.Api.Data;
using DevToolsLab.Api.Messaging;
using DevToolsLab.Api.Services;
using DevToolsLab.Core.Interfaces;
using MediatR;
using MongoDB.Driver;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using RabbitMQ.Client;
using Serilog;
using StackExchange.Redis;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSerilog();
builder.Host.UseSerilog((ctx, lc) => lc.ReadFrom.Configuration(ctx.Configuration));

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("DevToolsLab.Api"))
    .WithMetrics(m => m.AddConsoleExporter());

builder.Services.AddCors(o => o.AddDefaultPolicy(p =>
    p.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader()));

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));

builder.Services.AddSingleton<IMongoClient>(_ =>
    new MongoClient(builder.Configuration["MongoDb:ConnectionString"] ?? "mongodb://localhost:27017"));
builder.Services.AddSingleton(sp =>
{
    var client = sp.GetRequiredService<IMongoClient>();
    return client.GetDatabase(builder.Configuration["MongoDb:DatabaseName"] ?? "devtools");
});
builder.Services.AddSingleton<MongoRepository>();

builder.Services.AddSingleton<IConnectionMultiplexer>(_ =>
    ConnectionMultiplexer.Connect(builder.Configuration["Redis:ConnectionString"] ?? "localhost:6379"));
builder.Services.AddSingleton<RedisCache>();

builder.Services.AddSingleton<IConnection>(_ =>
{
    var factory = new ConnectionFactory { HostName = builder.Configuration["RabbitMQ:Host"] ?? "localhost" };
    return factory.CreateConnection();
});
builder.Services.AddSingleton<RabbitMqPublisher>();

builder.Services.AddScoped<IAiService>(sp =>
{
    var cfg = sp.GetRequiredService<IConfiguration>();
    return new AzureOpenAiService(
        cfg["AzureOpenAI:Endpoint"] ?? "",
        cfg["AzureOpenAI:ApiKey"] ?? "",
        cfg["AzureOpenAI:DeploymentName"] ?? "gpt-4");
});
builder.Services.AddScoped<IScannerService, ScannerService>();

builder.Services.AddControllers();

var app = builder.Build();
app.UseSwagger().UseSwaggerUI();
app.UseCors();
app.MapControllers();

await app.RunAsync();
