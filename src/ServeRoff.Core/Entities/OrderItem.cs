namespace ServeRoff.Core.Entities;

public class OrderItem : IEntity
{
    public Id Id { get; set; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    
    public virtual Order Order { get; set; } = null!;
    public virtual Product Product { get; set; } = null!;
}
