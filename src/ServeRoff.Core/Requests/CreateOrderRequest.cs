namespace ServeRoff.Core.Requests;

public record CreateOrderRequest(
    string CustomerName,
    string PhoneNumber,
    OrderItemRequest[] Items
) : IRequest;

public record OrderItemRequest(
    Guid ProductId,
    int Quantity
);
