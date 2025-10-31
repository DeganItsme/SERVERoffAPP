using ServeRoff.Application.Interfaces;

namespace ServeRoff.Application.Products.Commands;

public class GetAllProductsCommand : ICommand<EmptyRequest, ProductsResponse>
{
    private readonly IRepository<Product> _productRepository;

    public GetAllProductsCommand(IRepository<Product> productRepository)
    {
        _productRepository = productRepository;
    }

    public async Task<ProductsResponse> ExecuteAsync(
        EmptyRequest request, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            var products = await _productRepository.GetAllAsync(cancellationToken);
            
            var productResponses = products.Select(p => new ProductResponse(
                p.Id.Value,
                p.Name,
                p.Description,
                p.Price,
                p.Category,
                p.IsAvailable
            ));

            return new ProductsResponse(200, "OK", productResponses);
        }
        catch (Exception)
        {
            return new ProductsResponse(500, "Internal server error", []);
        }
    }
}
