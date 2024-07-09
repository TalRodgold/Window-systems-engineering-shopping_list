using Microsoft.EntityFrameworkCore;
using shopping_server.Models;

namespace shopping_server.Commands;

public class FoodCommand : IFoodCommand
{
    private readonly FoodContext _dbContext;

    public FoodCommand(FoodContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<Food> CreateFoodAsync(Food food)
    {
        _dbContext.Foods.Add(food);
        await _dbContext.SaveChangesAsync();
        return food;
    }

    public async Task<bool> UpdateFoodAsync(int id, Food food)
    {
        if (id != food.Id)
            return false;

        _dbContext.Entry(food).State = EntityState.Modified;

        try
        {
            await _dbContext.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!FoodExists(id))
                return false;

            throw;
        }
        return true;
    }

    public async Task<bool> DeleteFoodAsync(int id)
    {
        var food = await _dbContext.Foods.FindAsync(id);
        if (food == null)
            return false;

        _dbContext.Foods.Remove(food);
        await _dbContext.SaveChangesAsync();
        return true;
    }

    private bool FoodExists(int id)
    {
        return _dbContext.Foods.Any(f => f.Id == id);
    }
}
