using shopping_server.Models;

namespace shopping_server.Commands;

public interface IFoodCommand
{
    Task<Food> CreateFoodAsync(Food food);
    Task<bool> UpdateFoodAsync(int id, Food food);
    Task<bool> DeleteFoodAsync(int id);
}
