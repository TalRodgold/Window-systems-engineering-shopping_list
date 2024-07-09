using Microsoft.EntityFrameworkCore;
using shopping_server.Commands;
using shopping_server.Models;
using shopping_server.Qureries;
namespace shopping_server;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        builder.Services.AddDbContext<FoodContext>(options =>
            options.UseSqlServer(builder.Configuration.GetConnectionString("FoodContext")));

        builder.Services.AddScoped<IFoodCommand, FoodCommand>();
        builder.Services.AddScoped<IFoodQuery, FoodQuery>();

        builder.Services.AddControllers();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();

        var app = builder.Build();


        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseHttpsRedirection();

        app.UseAuthorization();


        app.MapControllers();

        app.Run();
    }
}
