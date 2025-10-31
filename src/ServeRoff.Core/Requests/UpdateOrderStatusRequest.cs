namespace ServeRoff.Core.Requests;

public record UpdateOrderStatusRequest(
    Guid OrderId,
    OrderStatus Status
) : IRequest;
