"""Product search tool using RAG (Retrieval Augmented Generation)."""
from typing import Any, Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.rag.simple_embedder import get_vector_store


class ProductSearchInput(BaseModel):
    """Input for ProductSearchTool."""
    query: str = Field(description="search query for finding products (e.g., 'tumbler', 'large bottle', 'glass cup')")


class ProductSearchTool(BaseTool):
    """
    A tool that searches for ZUS Coffee drinkware products using RAG.
    Uses semantic search to find relevant products based on user queries.
    """
    name: str = "product_search"
    description: str = (
        "useful for finding ZUS Coffee drinkware products like tumblers, bottles, mugs, and cups. "
        "Use this when users ask about products, prices, features, or what's available to buy."
    )
    args_schema: Type[BaseModel] = ProductSearchInput

    def _run(self, query: str) -> str:
        """
        Search for products matching the query.
        
        Args:
            query: Search query string
            
        Returns:
            Formatted string with product information
        """
        try:
            vector_store = get_vector_store()
            results = vector_store.search(query, top_k=3)
            
            if not results:
                return "I couldn't find any products matching your query. We have tumblers, bottles, mugs, and other drinkware available."
            
            # Format results into a readable response
            response_parts = [f"I found {len(results)} products that match your query:\n"]
            
            for idx, product in enumerate(results, 1):
                response_parts.append(f"\n{idx}. **{product['name']}**")
                response_parts.append(f"   - Price: RM {product['price_myr']:.2f}")
                response_parts.append(f"   - Capacity: {product['capacity_ml']}ml")
                response_parts.append(f"   - Material: {product['material']}")
                
                if product.get('colors'):
                    colors = ', '.join(product['colors'][:3])  # Show first 3 colors
                    response_parts.append(f"   - Colors: {colors}")
                
                if product.get('description'):
                    # Show first 100 chars of description
                    desc = product['description'][:100] + "..." if len(product['description']) > 100 else product['description']
                    response_parts.append(f"   - Description: {desc}")
                
                if product.get('in_stock') is False:
                    response_parts.append(f"   - **Currently out of stock**")
            
            return '\n'.join(response_parts)
            
        except Exception as e:
            print(f"Error in product search: {e}")
            return f"I encountered an error while searching for products: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)

