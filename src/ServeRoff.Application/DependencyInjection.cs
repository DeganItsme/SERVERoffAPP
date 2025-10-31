using Microsoft.Extensions.DependencyInjection;
using ServeRoff.Application.Interfaces;
using ServeRoff.Application.Orders.Commands;
using ServeRoff.Application.Products.Commands;

namespace ServeRoff.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        // Регистрируем команды
        services.AddScoped<CreateProductCommand>();
        services.AddScoped<GetAllProductsCommand>();
        services.AddScoped<CreateOrderCommand>();

        return services;
    }
}
