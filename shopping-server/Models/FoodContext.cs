using Microsoft.EntityFrameworkCore;

namespace shopping_server.Models;

public class FoodContext: DbContext
{
    public FoodContext(DbContextOptions<FoodContext> options) : base(options) { }

    public DbSet<Food> Foods { get; set; } = null!;
}
