#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
个人所得税计算器
实现2024年最新个税计算规则
"""

class TaxCalculator:
    def __init__(self):
        # 年度累计预扣预缴税率表
        self.annual_tax_brackets = [
            (0, 36000, 0.03, 0),        # 不超过36000元的部分
            (36000, 144000, 0.10, 2520),  # 超过36000元至144000元的部分
            (144000, 300000, 0.20, 16920), # 超过144000元至300000元的部分
            (300000, 420000, 0.25, 31920), # 超过300000元至420000元的部分
            (420000, 660000, 0.30, 52920), # 超过420000元至660000元的部分
            (660000, 960000, 0.35, 85920), # 超过660000元至960000元的部分
            (960000, float('inf'), 0.45, 181920) # 超过960000元的部分
        ]
        
        # 每月基本减除费用
        self.basic_deduction = 5000
        
    def calculate_accumulated_tax(self, accumulated_income: float, accumulated_deduction: float, 
                                previous_tax: float = 0) -> float:
        """
        计算累计预扣预缴应纳税额
        
        Args:
            accumulated_income: 累计收入
            accumulated_deduction: 累计扣除额（含基本减除费用）
            previous_tax: 之前已预缴的税额
            
        Returns:
            当前应缴纳的税额
        """
        # 计算累计应纳税所得额
        taxable_income = accumulated_income - accumulated_deduction
        
        if taxable_income <= 0:
            return 0
            
        # 查找适用税率和速算扣除数
        for lower, upper, rate, deduction in self.annual_tax_brackets:
            if lower < taxable_income <= upper:
                # 计算累计应纳税额
                total_tax = taxable_income * rate - deduction
                # 扣除已预缴税额
                current_tax = total_tax - previous_tax
                return max(current_tax, 0)
                
        return 0
        
    def calculate_monthly_tax(self, month: int, monthly_income: float, special_deductions: dict) -> float:
        """
        计算月度个税
        
        Args:
            month: 当前月份（1-12）
            monthly_income: 当月收入
            special_deductions: 专项附加扣除字典，包含：
                - children_education: 子女教育
                - housing_loan: 住房贷款利息
                - elderly_care: 赡养老人
                - other: 其他扣除（如商业健康保险等）
        
        Returns:
            当月应缴纳的税额
        """
        # 计算累计收入
        accumulated_income = monthly_income * month
        
        # 计算累计专项附加扣除
        monthly_deductions = (
            special_deductions.get('children_education', 0) +
            special_deductions.get('housing_loan', 0) +
            special_deductions.get('elderly_care', 0) +
            special_deductions.get('other', 0)
        )
        accumulated_deductions = (self.basic_deduction + monthly_deductions) * month
        
        # 计算之前月份已预缴税额
        if month > 1:
            previous_tax = self.calculate_accumulated_tax(
                accumulated_income - monthly_income,
                accumulated_deductions - (self.basic_deduction + monthly_deductions)
            )
        else:
            previous_tax = 0
            
        # 计算当月应缴税额
        current_tax = self.calculate_accumulated_tax(
            accumulated_income,
            accumulated_deductions,
            previous_tax
        )
        
        return current_tax
        
    def calculate_bonus_tax(self, bonus: float) -> float:
        """
        计算年终奖个税（单独计税方法）
        
        Args:
            bonus: 年终奖金额
            
        Returns:
            应缴纳的税额
        """
        # 将年终奖除以12计算适用税率
        monthly_equivalent = bonus / 12
        
        # 查找适用税率和速算扣除数
        for lower, upper, rate, deduction in self.annual_tax_brackets:
            if lower / 12 < monthly_equivalent <= upper / 12:
                return bonus * rate - deduction
                
        return 0
        
    def optimize_bonus_plan(self, annual_salary: float, bonus: float, 
                          monthly_deductions: float) -> dict:
        """
        优化年终奖方案，对比并入年收入和单独计算两种方案
        
        Args:
            annual_salary: 年度工资收入
            bonus: 年终奖金额
            monthly_deductions: 月度专项附加扣除总额
            
        Returns:
            包含两种方案的详细计算结果和建议
        """
        # 方案1：年终奖并入年收入
        combined_annual = annual_salary + bonus
        monthly_combined = combined_annual / 12
        accumulated_deductions = (self.basic_deduction + monthly_deductions) * 12
        combined_tax = self.calculate_accumulated_tax(combined_annual, accumulated_deductions)
        combined_net = combined_annual - combined_tax
        
        # 方案2：年终奖单独计算
        accumulated_deductions = (self.basic_deduction + monthly_deductions) * 12
        annual_tax = self.calculate_accumulated_tax(annual_salary, accumulated_deductions)
        bonus_tax = self.calculate_bonus_tax(bonus)
        separate_total_tax = annual_tax + bonus_tax
        separate_net = annual_salary + bonus - separate_total_tax
        
        return {
            'combined': {
                'tax': combined_tax,
                'net_income': combined_net
            },
            'separate': {
                'tax': separate_total_tax,
                'net_income': separate_net
            },
            'recommendation': 'combined' if combined_net > separate_net else 'separate'
        }

def format_money(amount: float) -> str:
    """格式化金额显示"""
    return f"{amount:,.2f}"

def main():
    calculator = TaxCalculator()
    
    while True:
        print("\n" + "="*50)
        print("个人所得税计算器")
        print("="*50)
        print("1. 计算月度个税")
        print("2. 计算年终奖方案")
        print("3. 退出")
        print("="*50)
        
        choice = input("\n请选择功能（1-3）：")
        
        if choice == "1":
            try:
                monthly_salary = float(input("请输入月收入（元）："))
                deductions = float(input("请输入月度专项附加扣除总额（元）："))
                
                monthly_tax = calculator.calculate_monthly_tax(monthly_salary, deductions)
                print("\n计算结果：")
                print(f"应缴纳月度个税：{format_money(monthly_tax)}元")
                print(f"税后收入：{format_money(monthly_salary - monthly_tax)}元")
            except ValueError:
                print("错误：请输入有效的数字！")
                
        elif choice == "2":
            try:
                annual_salary = float(input("请输入年度工资收入（元）："))
                bonus = float(input("请输入年终奖金额（元）："))
                
                optimization = calculator.optimize_bonus_plan(annual_salary, bonus, 0)
                
                print("\n=== 奖金方案对比 ===")
                print(f"方案1 - 并入年收入：")
                print(f"应缴税：{format_money(optimization['combined']['tax'])}元")
                print(f"税后收入：{format_money(optimization['combined']['net_income'])}元")
                
                print(f"\n方案2 - 单独计算：")
                print(f"应缴税：{format_money(optimization['separate']['tax'])}元")
                print(f"税后收入：{format_money(optimization['separate']['net_income'])}元")
                
                print(f"\n建议方案：{'并入年收入' if optimization['recommendation'] == 'combined' else '单独计算'}")
            except ValueError:
                print("错误：请输入有效的数字！")
                
        elif choice == "3":
            print("\n感谢使用！再见！")
            break
        else:
            print("无效的选择，请重试！")

def calculate_tax(salary=0, salary_type='monthly', bonus=0, bonus_type='separate',
                 labor_income=0, manuscript_income=0, license_income=0,
                 social_security_base=0, housing_fund_rate=0,
                 special_deductions=None):
    """
    计算个人所得税
    
    Args:
        salary: 工资收入
        salary_type: 工资类型（'monthly' 或 'annual'）
        bonus: 年终奖
        bonus_type: 奖金计税方式（'separate' 或 'combined'）
        labor_income: 劳务报酬
        manuscript_income: 稿酬收入
        license_income: 特许权使用费
        social_security_base: 社保缴纳基数
        housing_fund_rate: 公积金缴纳比例
        special_deductions: 专项附加扣除字典
    
    Returns:
        包含计算结果的字典
    """
    calculator = TaxCalculator()
    
    # 处理专项附加扣除
    if special_deductions is None:
        special_deductions = {}
    
    # 计算年度工资收入
    if salary_type == 'monthly':
        annual_salary = salary * 12
    else:
        annual_salary = salary
    
    # 计算社保和公积金
    monthly_social_security = social_security_base * 0.205  # 假设社保总比例为20.5%
    monthly_housing_fund = social_security_base * (housing_fund_rate / 100)
    annual_deductions = (monthly_social_security + monthly_housing_fund) * 12
    
    # 计算专项附加扣除总额
    monthly_special_deductions = sum(special_deductions.values())
    annual_special_deductions = monthly_special_deductions * 12
    
    # 计算工资薪金所得税
    salary_taxable_income = annual_salary - annual_deductions - annual_special_deductions - (calculator.basic_deduction * 12)
    salary_tax = calculator.calculate_accumulated_tax(annual_salary, annual_deductions + annual_special_deductions + (calculator.basic_deduction * 12))
    
    # 计算年终奖个税
    if bonus_type == 'separate':
        bonus_tax = calculator.calculate_bonus_tax(bonus)
        bonus_taxable_income = bonus
    else:
        # 并入年收入计算
        total_income = annual_salary + bonus
        total_tax = calculator.calculate_accumulated_tax(total_income, annual_deductions + annual_special_deductions + (calculator.basic_deduction * 12))
        bonus_tax = total_tax - salary_tax
        bonus_taxable_income = bonus
    
    # 计算其他收入的税款
    labor_tax = labor_income * 0.2 if labor_income > 0 else 0
    manuscript_tax = manuscript_income * 0.14 if manuscript_income > 0 else 0  # 稿酬所得适用70%计税
    license_tax = license_income * 0.2 if license_income > 0 else 0
    
    # 计算总税额和税后收入
    total_tax = salary_tax + bonus_tax + labor_tax + manuscript_tax + license_tax
    total_income = annual_salary + bonus + labor_income + manuscript_income + license_income
    net_income = total_income - total_tax - annual_deductions
    
    return {
        'salary_taxable_income': salary_taxable_income,
        'salary_tax': salary_tax,
        'bonus_taxable_income': bonus_taxable_income,
        'bonus_tax': bonus_tax,
        'labor_income': labor_income,
        'labor_tax': labor_tax,
        'manuscript_income': manuscript_income,
        'manuscript_tax': manuscript_tax,
        'license_income': license_income,
        'license_tax': license_tax,
        'total_taxable_income': total_income - annual_deductions - (calculator.basic_deduction * 12),
        'total_tax': total_tax,
        'total_deductions': annual_deductions + annual_special_deductions + (calculator.basic_deduction * 12),
        'net_income': net_income
    }

if __name__ == "__main__":
    main() 