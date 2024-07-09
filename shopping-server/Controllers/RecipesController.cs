using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace shopping_server.Controllers;

[Route("api/[controller]")]
[ApiController]
public class RecipesController : ControllerBase
{
    private static readonly string RECEIPES_API = "https://edamam-recipe-search.p.rapidapi.com/api/recipes/v2";
    private static readonly Dictionary<string, string> RECEIPES_HEADERS = new Dictionary<string, string>
        {
            { "Accept-Language", "en" },
            { "X-RapidAPI-Key", "e4cb194fedmsh8f5e57ba5fc557cp16248ajsn0d64d197f11a" },
            { "X-RapidAPI-Host", "edamam-recipe-search.p.rapidapi.com" }
        };
    private static readonly Dictionary<string, string> RECEIPES_QUERYSTRING = new Dictionary<string, string>
        {
            { "type", "public" },
            { "co2EmissionsClass", "A+" },
            { "field[0]", "uri" },
            { "q", "" },
            { "beta", "true" },
            { "random", "true" }
        };

    [HttpGet]
    public async Task<IActionResult> GetRecipes(string items)
    {
        try
        {
            var queryWithItems = new Dictionary<string, string>(RECEIPES_QUERYSTRING);
            foreach (var item in items.Split(','))
            {
                queryWithItems["q"] += $"\"{item.Trim()}\",";
            }

            queryWithItems["q"] = queryWithItems["q"].TrimEnd(',');

            var queryString = new StringBuilder();
            foreach (var param in queryWithItems)
            {
                queryString.Append($"{param.Key}={System.Net.WebUtility.UrlEncode(param.Value)}&");
            }

            var query = queryString.ToString().TrimEnd('&');

            using (var client = new HttpClient())
            {
                foreach (var header in RECEIPES_HEADERS)
                {
                    client.DefaultRequestHeaders.Add(header.Key, header.Value);
                }

                var response = await client.GetAsync($"{RECEIPES_API}?{query}");
                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    var result = new List<string>();
                    var j = JObject.Parse(json);
                    foreach (var item in j["hits"]!)
                    {
                        result.Add(item["recipe"]!["url"]!.ToString());
                    }
                    return Ok(result);
                }
                else
                {
                    return StatusCode((int)response.StatusCode, response.ReasonPhrase);
                }
            }
        }
        catch (Exception e)
        {
            return StatusCode(500, e.Message);
        }
    }

    private string ParseUserInput(string unparsedStr)
    {
        try
        {
            var splitList = Regex.Split(unparsedStr, "[ ,]");
            var cleanedList = splitList.Where(s => s.All(char.IsLetter)).ToList();

            if (cleanedList.Count != splitList.Length)
            {
                var invalidStrings = splitList.Except(cleanedList);
                throw new System.Exception($"String(s) '{string.Join(", ", invalidStrings)}' contain non-letter characters.");
            }

            return string.Join(",", cleanedList);
        }
        catch (Exception e)
        {
            throw new System.Exception($"Error: {e.Message}");
        }
    }
}

