namespace ServeRoff.Core.Responses;

public record ProductResponse(
    Guid Id,
    string Name,
    string Description,
    decimal Price,
    ProductCategory Category,
    bool IsAvailable
) : IResponse;
