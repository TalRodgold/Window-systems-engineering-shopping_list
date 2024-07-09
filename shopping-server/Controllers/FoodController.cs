using Microsoft.AspNetCore.Mvc;
using shopping_server.Commands;
using shopping_server.Qureries;
using shopping_server.Models;

namespace shopping_server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FoodController : ControllerBase
    {
        private readonly IFoodCommand _foodCommand;
        private readonly IFoodQuery _foodQuery;

        public FoodController(IFoodCommand foodCommand, IFoodQuery foodQuery)
        {
            _foodCommand = foodCommand;
            _foodQuery = foodQuery;
        }

        // GET: api/Foods
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Food>>> GetFoods()
        {
            var foods = await _foodQuery.GetAllFoodsAsync();
            if (foods == null)
                return NotFound();

            return Ok(foods);
        }

        // GET: api/Foods/id
        [HttpGet("{id}")]
        public async Task<ActionResult<Food>> GetFood(int id)
        {
            var food = await _foodQuery.GetFoodByIdAsync(id);
            if (food == null)
                return NotFound();

            return Ok(food);
        }

        // POST: api/Foods
        [HttpPost]
        public async Task<ActionResult<Food>> PostFood(Food food)
        {
            var createdFood = await _foodCommand.CreateFoodAsync(food);
            return CreatedAtAction(nameof(GetFood), new { id = createdFood.Id }, createdFood);
        }

        // PUT: api/Foods/id
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFood(int id, [FromBody] Food food)
        {
            var result = await _foodCommand.UpdateFoodAsync(id, food);
            if (!result)
                return BadRequest();

            return NoContent();
        }

        // DELETE: api/Foods/DeleteById/id
        [HttpDelete("DeleteById/{id}")]
        public async Task<IActionResult> DeleteFood(int id)
        {
            var result = await _foodCommand.DeleteFoodAsync(id);
            if (!result)
                return NotFound();

            return NoContent();
        }
    }
}
