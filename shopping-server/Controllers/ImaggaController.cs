using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;
using shopping_server.Models;

namespace recipes_server.Controllers;

[Route("api/[controller]")]
[ApiController]
public class ImaggaController : ControllerBase
{
    private readonly string _apiKey = "acc_f7fdd2eb8b0f369";
    private readonly string _apiSecret = "fa10d16de4c930c643cfb106f4b3d0f2";

    [HttpGet("{imageUrl}")]
    public async Task<IActionResult> GetTags(string imageUrl)
    {
        if (string.IsNullOrEmpty(imageUrl))
        {
            return BadRequest("Image URL is required in the 'Image-Url' header.");
        }

        string apiUrl = $"https://api.imagga.com/v2/tags?image_url={imageUrl}";

        try
        {
            using (HttpClient client = new HttpClient())
            {
                // Set Imagga authorization header
                client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic",
                    Convert.ToBase64String(System.Text.Encoding.ASCII.GetBytes($"{_apiKey}:{_apiSecret}")));

                HttpResponseMessage response = await client.GetAsync(apiUrl);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    var data = JObject.Parse(responseBody);

                    List<string> tagList = new List<string>();

                    foreach (var tag in data["result"]!["tags"]!)
                    {
                        var probability = (float)tag["confidence"]!;

                        if (probability > 0.95)
                        {
                            var tagValue = tag["tag"]!["en"]!.ToString();
                            tagList.Add(tagValue);
                        }
                    }

                    if (tagList != null)
                    {
                        return Ok(tagList);
                    }
                    else
                    {
                        return NotFound("No tags found for the image.");
                    }
                }
                else
                {
                    return StatusCode((int)response.StatusCode, $"Failed to get response. Status code: {response.StatusCode}");
                }
            }
        }
        catch (Exception ex)
        {
            return BadRequest($"An error occurred: {ex.Message}");
        }
    }
}
