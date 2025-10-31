using Microsoft.Extensions.Logging;
using ServeRoff.Application.Interfaces;

namespace ServeRoff.Application.Products.Commands;

public class CreateProductCommand : ICommand<CreateProductRequest, BaseResponse>
{
    private readonly IRepository<Product> _productRepository;
    private readonly ILogger<CreateProductCommand> _logger;

    public CreateProductCommand(
        IRepository<Product> productRepository,
        ILogger<CreateProductCommand> logger)
    {
        _productRepository = productRepository;
        _logger = logger;
    }

    public async Task<BaseResponse> ExecuteAsync(
        CreateProductRequest request, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("Creating new product: {ProductName}", request.Name);

            var product = new Product
            {
                Id = new Id(Guid.NewGuid()),
                Name = request.Name,
                Description = request.Description,
                Price = request.Price,
                Category = request.Category,
                IsAvailable = true
            };

            await _productRepository.AddAsync(product, cancellationToken);
            await _productRepository.SaveChangesAsync(cancellationToken);

            _logger.LogInformation("Product created successfully: {ProductId}", product.Id.Value);
            
            return new BaseResponse(201, "Product created successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating product: {ProductName}", request.Name);
            return new BaseResponse(500, "An error occurred while creating the product");
        }
    }
}
