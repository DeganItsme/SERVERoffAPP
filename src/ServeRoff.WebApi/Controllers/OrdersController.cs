using Microsoft.AspNetCore.Mvc;
using ServeRoff.Application.Orders.Commands;
using ServeRoff.Core.Requests;

namespace ServeRoff.WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly CreateOrderCommand _createOrderCommand;

    public OrdersController(CreateOrderCommand createOrderCommand)
    {
        _createOrderCommand = createOrderCommand;
    }

    [HttpPost]
    public async Task<IActionResult> CreateOrder(CreateOrderRequest request)
    {
        var result = await _createOrderCommand.ExecuteAsync(request);
        return StatusCode(result.Code, result);
    }
}
