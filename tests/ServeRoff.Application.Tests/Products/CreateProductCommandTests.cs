using Moq;
using ServeRoff.Application.Interfaces;
using ServeRoff.Application.Products.Commands;
using ServeRoff.Core.Entities;
using ServeRoff.Core.Requests;

namespace ServeRoff.Application.Tests.Products;

public class CreateProductCommandTests
{
    [Test]
    public async Task ExecuteAsync_WhenProductIsValid_ReturnsSuccess()
    {
        // Arrange
        var mockRepository = new Mock<IRepository<Product>>();
        var mockLogger = new Mock<ILogger<CreateProductCommand>>();
        
        var command = new CreateProductCommand(mockRepository.Object, mockLogger.Object);
        var request = new CreateProductRequest("Нон", "Свежий узбекский нон", 5000, ProductCategory.Bread);

        // Act
        var result = await command.ExecuteAsync(request);

        // Assert
        Assert.That(result.Code, Is.EqualTo(201));
        Assert.That(result.Description, Is.EqualTo("Product created successfully"));
        
        mockRepository.Verify(r => r.AddAsync(It.IsAny<Product>(), It.IsAny<CancellationToken>()), Times.Once);
        mockRepository.Verify(r => r.SaveChangesAsync(It.IsAny<CancellationToken>()), Times.Once);
    }
}
