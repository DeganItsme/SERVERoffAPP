using Microsoft.Extensions.Logging;
using ServeRoff.Application.Interfaces;

namespace ServeRoff.Application.Orders.Commands;

public class CreateOrderCommand : ICommand<CreateOrderRequest, BaseResponse>
{
    private readonly IRepository<Order> _orderRepository;
    private readonly IRepository<Product> _productRepository;
    private readonly ILogger<CreateOrderCommand> _logger;

    public CreateOrderCommand(
        IRepository<Order> orderRepository,
        IRepository<Product> productRepository,
        ILogger<CreateOrderCommand> logger)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _logger = logger;
    }

    public async Task<BaseResponse> ExecuteAsync(
        CreateOrderRequest request, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("Creating order for customer: {CustomerName}", request.CustomerName);

            var order = new Order
            {
                Id = new Id(Guid.NewGuid()),
                CustomerName = request.CustomerName,
                PhoneNumber = request.PhoneNumber,
                Status = OrderStatus.Pending
            };

            decimal totalAmount = 0;
            var orderItems = new List<OrderItem>();

            foreach (var item in request.Items)
            {
                var product = await _productRepository.GetByIdAsync(item.ProductId, cancellationToken);
                
                if (product == null || !product.IsAvailable)
                {
                    return new BaseResponse(400, $"Product with ID {item.ProductId} not found or unavailable");
                }

                var orderItem = new OrderItem
                {
                    Id = new Id(Guid.NewGuid()),
                    Product = product,
                    Quantity = item.Quantity,
                    UnitPrice = product.Price,
                    Order = order
                };

                orderItems.Add(orderItem);
                totalAmount += product.Price * item.Quantity;
            }

            order.OrderItems = orderItems;
            order.TotalAmount = totalAmount;

            await _orderRepository.AddAsync(order, cancellationToken);
            await _orderRepository.SaveChangesAsync(cancellationToken);

            _logger.LogInformation("Order created successfully: {OrderId}", order.Id.Value);
            
            return new BaseResponse(201, "Order created successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating order for customer: {CustomerName}", request.CustomerName);
            return new BaseResponse(500, "An error occurred while creating the order");
        }
    }
}
