using Microsoft.AspNetCore.Mvc;
using ServeRoff.Application.Products.Commands;
using ServeRoff.Core.Requests;

namespace ServeRoff.WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly CreateProductCommand _createProductCommand;
    private readonly GetAllProductsCommand _getAllProductsCommand;

    public ProductsController(
        CreateProductCommand createProductCommand,
        GetAllProductsCommand getAllProductsCommand)
    {
        _createProductCommand = createProductCommand;
        _getAllProductsCommand = getAllProductsCommand;
    }

    [HttpGet]
    public async Task<IActionResult> GetProducts()
    {
        var result = await _getAllProductsCommand.ExecuteAsync(new EmptyRequest());
        return StatusCode(result.Code, result);
    }

    [HttpPost]
    public async Task<IActionResult> CreateProduct(CreateProductRequest request)
    {
        var result = await _createProductCommand.ExecuteAsync(request);
        return StatusCode(result.Code, result);
    }
}
