import chromadb
import os
from typing import List, Dict

def create_sample_data() -> List[Dict[str, str]]:
    """Create sample company knowledge data"""
    return [
        {
            "id": "1",
            "document": "Our business hours are Monday through Friday, 9:00 AM to 6:00 PM EST. We are closed on weekends and major holidays.",
            "metadata": {"category": "business_hours", "topic": "hours"}
        },
        {
            "id": "2",
            "document": "To get a simple quote for our products, please provide: 1) Product name or SKU, 2) Quantity needed, 3) Delivery timeline. Our sales team will respond within 24 hours with a detailed quote.",
            "metadata": {"category": "quotes", "topic": "process"}
        },
        {
            "id": "3",
            "document": "Our return policy allows returns within 30 days of purchase. Items must be in original condition with all packaging. Refunds are processed within 5-7 business days after we receive the returned item.",
            "metadata": {"category": "returns", "topic": "policy"}
        },
        {
            "id": "4",
            "document": "We offer three main product lines: Enterprise Solutions (for large businesses), Professional Tools (for small to medium businesses), and Starter Kits (for individuals and startups). Each line includes software licenses, training, and support.",
            "metadata": {"category": "products", "topic": "overview"}
        },
        {
            "id": "5",
            "document": "For technical support, email support@company.com or call 1-800-TECH-HELP. Premium customers have access to 24/7 support, while standard customers can reach us during business hours.",
            "metadata": {"category": "support", "topic": "contact"}
        },
        {
            "id": "6",
            "document": "Payment methods accepted include: credit cards (Visa, MasterCard, American Express), ACH transfers, wire transfers, and purchase orders for qualified businesses. Payment terms are Net 30 for approved accounts.",
            "metadata": {"category": "payment", "topic": "methods"}
        },
        {
            "id": "7",
            "document": "Standard shipping takes 5-7 business days. Express shipping (2-3 days) and overnight options are available for an additional fee. International shipping is available to select countries with delivery times varying by location.",
            "metadata": {"category": "shipping", "topic": "options"}
        }
    ]

def seed_database():
    """Create and populate the ChromaDB database"""
    # Create persistent client
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete collection if it exists (for fresh start)
    try:
        client.delete_collection(name="company_knowledge")
        print("Deleted existing collection")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        name="company_knowledge",
        metadata={"description": "Company knowledge base for E-180R"}
    )
    
    # Get sample data
    sample_data = create_sample_data()
    
    # Prepare data for insertion
    documents = []
    metadatas = []
    ids = []
    
    for item in sample_data:
        documents.append(item["document"])
        metadatas.append(item["metadata"])
        ids.append(item["id"])
    
    # Add documents to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Successfully added {len(documents)} documents to the collection")
    
    # Verify the database
    results = collection.get()
    print(f"\nVerification: Found {len(results['ids'])} documents in the database")
    print("\nSample entries:")
    for i in range(min(3, len(results['ids']))):
        print(f"\nID: {results['ids'][i]}")
        print(f"Document: {results['documents'][i][:100]}...")
        print(f"Metadata: {results['metadatas'][i]}")

if __name__ == "__main__":
    seed_database()
    print("\nDatabase seeding completed successfully!")
    print("ChromaDB files created in ./chroma_db directory") 