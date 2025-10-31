namespace ServeRoff.Core.Responses;

public record ProductsResponse(
    int Code,
    string Description,
    IEnumerable<ProductResponse> Products
) : BaseResponse(Code, Description);
