"""
Example Usage of CrewAI Data Analysis Crew with Keboola MCP Server

This script demonstrates various ways to use the Keboola Data Analysis Crew
for different types of data analysis tasks.
"""

import asyncio
from data_analysis_crew import KeboolaDataAnalysisCrew


async def example_comprehensive_analysis():
    """Example 1: Comprehensive data analysis across all aspects."""
    print("🔍 Example 1: Comprehensive Data Analysis")
    print("=" * 50)
    
    crew = KeboolaDataAnalysisCrew()
    
    result = await crew.run_analysis(
        custom_objective="""
        Perform a comprehensive analysis of our data ecosystem:
        1. Understand the complete data landscape
        2. Identify key business metrics and KPIs
        3. Assess data quality and completeness
        4. Optimize existing data pipelines
        5. Provide actionable recommendations for data strategy
        """
    )
    
    print("📊 Results:")
    print(result)
    return result


async def example_customer_analysis():
    """Example 2: Customer-focused analysis."""
    print("\n👥 Example 2: Customer Analysis Focus")
    print("=" * 50)
    
    crew = KeboolaDataAnalysisCrew()
    
    result = await crew.run_analysis(
        custom_objective="""
        Focus specifically on customer data analysis:
        1. Find all customer-related tables and data sources
        2. Perform customer segmentation analysis
        3. Calculate customer lifetime value and retention metrics
        4. Identify trends in customer behavior
        5. Create customer analytics transformations if needed
        """
    )
    
    print("👥 Customer Analysis Results:")
    print(result)
    return result


async def example_sales_performance():
    """Example 3: Sales performance analysis."""
    print("\n💰 Example 3: Sales Performance Analysis")
    print("=" * 50)
    
    crew = KeboolaDataAnalysisCrew()
    
    result = await crew.run_analysis(
        custom_objective="""
        Analyze sales performance and revenue trends:
        1. Identify all sales and revenue related data
        2. Calculate key sales metrics (revenue, growth, conversion rates)
        3. Analyze sales trends over time
        4. Identify top performing products/regions/channels
        5. Create sales reporting transformations
        """
    )
    
    print("💰 Sales Analysis Results:")
    print(result)
    return result


async def example_data_quality_audit():
    """Example 4: Data quality and pipeline health audit."""
    print("\n🔧 Example 4: Data Quality & Pipeline Audit")
    print("=" * 50)
    
    crew = KeboolaDataAnalysisCrew()
    
    result = await crew.run_analysis(
        custom_objective="""
        Conduct a thorough data quality and pipeline health audit:
        1. Assess data quality across all tables (completeness, accuracy, consistency)
        2. Review all existing transformations and their performance
        3. Analyze job execution history for failures and bottlenecks
        4. Identify data governance issues
        5. Recommend pipeline optimizations and data quality improvements
        """
    )
    
    print("🔧 Data Quality Audit Results:")
    print(result)
    return result


async def example_quick_data_exploration():
    """Example 5: Quick data exploration for new projects."""
    print("\n🚀 Example 5: Quick Data Exploration")
    print("=" * 50)
    
    crew = KeboolaDataAnalysisCrew()
    
    result = await crew.run_analysis(
        custom_objective="""
        Perform a quick exploration of available data for a new project:
        1. List all available data sources and their purposes
        2. Identify the most valuable datasets for analysis
        3. Understand data relationships and dependencies
        4. Suggest initial analysis opportunities
        5. Provide a data discovery summary for stakeholders
        """
    )
    
    print("🚀 Quick Exploration Results:")
    print(result)
    return result


async def main():
    """Main function to run different examples."""
    print("🤖 Keboola Data Analysis Crew - Example Usage")
    print("=" * 60)
    
    examples = [
        ("Comprehensive Analysis", example_comprehensive_analysis),
        ("Customer Analysis", example_customer_analysis),
        ("Sales Performance", example_sales_performance),
        ("Data Quality Audit", example_data_quality_audit),
        ("Quick Data Exploration", example_quick_data_exploration),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\nChoose an example to run (1-5), or 'all' to run all examples:")
    choice = input("Enter your choice: ").strip().lower()
    
    try:
        if choice == 'all':
            print("\n🚀 Running all examples...")
            for name, example_func in examples:
                print(f"\n{'='*80}")
                print(f"Running: {name}")
                print('='*80)
                await example_func()
                print(f"\n✅ Completed: {name}")
                
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            example_index = int(choice) - 1
            name, example_func = examples[example_index]
            print(f"\n🚀 Running: {name}")
            await example_func()
            
        else:
            print("❌ Invalid choice. Please enter 1-5 or 'all'.")
            return
    
    except Exception as e:
        print(f"❌ Error running example: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("🎉 Example execution completed!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main()) 