using shopping_server.Models;

namespace shopping_server.Qureries;

public interface IFoodQuery
{
    Task<IEnumerable<Food>> GetAllFoodsAsync();
    Task<Food?> GetFoodByIdAsync(int id);
}
