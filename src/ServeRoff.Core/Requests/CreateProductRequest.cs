namespace ServeRoff.Core.Requests;

public record CreateProductRequest(
    string Name,
    string Description,
    decimal Price,
    ProductCategory Category
) : IRequest;
