using Microsoft.EntityFrameworkCore;
using shopping_server.Models;
using shopping_server.Qureries;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

public class FoodQuery : IFoodQuery
{
    private readonly FoodContext _dbContext;

    public FoodQuery(FoodContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<IEnumerable<Food>> GetAllFoodsAsync()
    {
        return await _dbContext.Foods.ToListAsync();
    }

    public async Task<Food?> GetFoodByIdAsync(int id)
    {
        return await _dbContext.Foods.FindAsync(id);
    }
}
