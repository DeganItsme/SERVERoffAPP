using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using ServeRoff.Application.Interfaces;
using ServeRoff.Infrastructure.Data;
using ServeRoff.Infrastructure.Repositories;

namespace ServeRoff.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services)
    {
        // Используем InMemory database для простоты
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseInMemoryDatabase("ServeRoffDb"));

        // Регистрируем репозитории
        services.AddScoped(typeof(IRepository<>), typeof(EFRepository<>));

        return services;
    }
}
