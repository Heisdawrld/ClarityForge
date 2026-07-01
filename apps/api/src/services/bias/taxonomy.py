from pydantic import BaseModel


class BiasDefinition(BaseModel):
    type: str
    name: str
    description: str
    examples: list[str]
    mitigation: str
    category: str = "cognitive"


BIAS_TAXONOMY = [
    BiasDefinition(
        type="confirmation",
        name="Confirmation Bias",
        description="The tendency to search for, interpret, favor, and recall information in a way that confirms or supports one's prior beliefs or values.",
        examples=[
            "Only reading news sources that align with your political views",
            "Asking friends who agree with your business idea for feedback",
        ],
        mitigation="Actively seek out opposing viewpoints and Devil's advocate arguments.",
        category="cognitive",
    ),
    BiasDefinition(
        type="anchoring",
        name="Anchoring Bias",
        description="The cognitive bias where an individual depends too heavily on an initial piece of information offered to make subsequent judgments during decision making.",
        examples=[
            "Getting fixated on the first salary number in negotiations",
            "Judging a stock's value based on its opening price",
        ],
        mitigation="Make decisions without initial reference points when possible. Use diverse sources.",
        category="cognitive",
    ),
    BiasDefinition(
        type="availability",
        name="Availability Heuristic",
        description="A mental shortcut that relies on immediate examples that come to a given person's mind when evaluating a specific topic, concept, method or decision.",
        examples=[
            "Overestimating the likelihood of plane crashes after seeing news coverage",
            "Thinking entrepreneurship is common because of media coverage of startups",
        ],
        mitigation="Use statistical data rather than anecdotal evidence. Consider base rates.",
        category="heuristic",
    ),
    BiasDefinition(
        type="survivorship",
        name="Survivorship Bias",
        description="The logical error of concentrating on the people or things that made it past some selection process and overlooking those that did not, typically because of their lack of visibility.",
        examples=[
            "Studying successful entrepreneurs without examining the failed ones",
            "Learning from business books about successful companies only",
        ],
        mitigation="Include failed cases in analysis. Ask what failed and why.",
        category="selection",
    ),
    BiasDefinition(
        type="sunk_cost",
        name="Sunk Cost Fallacy",
        description="The phenomenon whereby a person is reluctant to abandon a strategy or course of action because they have invested heavily in it, even when it is clear that abandonment would be more beneficial.",
        examples=[
            "Continuing to fund a failing project because of prior investments",
            "Watching a bad movie just because you already paid for the ticket",
        ],
        mitigation="Focus on future costs and benefits, not past investments.",
        category="decision",
    ),
    BiasDefinition(
        type="status_quo",
        name="Status Quo Bias",
        description="The preference for the current state of affairs. The current baseline (or status quo) is taken as a reference point, and any change from that baseline is perceived as a loss.",
        examples=[
            "Staying in a job you're unhappy with just because it's familiar",
            "Keeping old processes in place despite better alternatives",
        ],
        mitigation="Evaluate options as if starting fresh. Ask what you would choose today.",
        category="decision",
    ),
    BiasDefinition(
        type="bandwagon",
        name="Bandwagon Effect",
        description="The tendency to do (or believe) things because many other people do (or believe) the same. The probability of one person adopting a belief increases as more people adopt it.",
        examples=[
            "Investing in a hot startup because everyone else is",
            "Choosing a career because it's trendy",
        ],
        mitigation="Make decisions based on fundamentals, not popularity. Develop independent criteria.",
        category="social",
    ),
    BiasDefinition(
        type="halo",
        name="Halo Effect",
        description="The tendency for an impression created in one area to influence opinion in another area.",
        examples=[
            "Assuming a attractive person is also intelligent and kind",
            "Judging a company positively because of its sleek office design",
        ],
        mitigation="Evaluate each dimension independently. Use structured criteria.",
        category="perception",
    ),
    BiasDefinition(
        type="authority",
        name="Authority Bias",
        description="The tendency to attribute greater accuracy to the opinion of an authority figure and be more influenced by that opinion.",
        examples=[
            "Accepting expert advice without independent verification",
            "Following company leadership blindly into a new strategy",
        ],
        mitigation="Challenge authority figures. Evaluate evidence independently.",
        category="social",
    ),
    BiasDefinition(
        type="groupthink",
        name="Groupthink",
        description="The practice of thinking or making decisions as a group in a way that discourages creativity or individual responsibility.",
        examples=[
            "Board members not voicing concerns about a risky acquisition",
            "Engineering team agreeing with the lead architect without debate",
        ],
        mitigation="Encourage dissent. Use pre-mortems and anonymous feedback.",
        category="group",
    ),
    BiasDefinition(
        type="overconfidence",
        name="Overconfidence Bias",
        description="A cognitive bias where one's subjective confidence in their judgments is greater than their objective accuracy.",
        examples=[
            "Underestimating project completion time",
            "Overestimating your ability to predict market movements",
        ],
        mitigation="Calibrate estimates against historical data. Seek outside opinions.",
        category="cognitive",
    ),
    BiasDefinition(
        type="planning",
        name="Planning Fallacy",
        description="The tendency to underestimate the time, costs, and risks of future actions while overestimating the benefits.",
        examples=[
            "Software projects consistently exceeding estimates",
            "Home renovation projects always taking longer than planned",
        ],
        mitigation="Use reference class forecasting. Include buffer for unknowns.",
        category="estimation",
    ),
    BiasDefinition(
        type="outcome",
        name="Outcome Bias",
        description="Judging a decision based on the outcome rather than the quality of the decision at the time it was made.",
        examples=[
            "Praising a risky bet that happened to work out",
            "Blaming a manager for a bad outcome that couldn't have been predicted",
        ],
        mitigation="Focus on decision process, not just outcomes. Use premortems.",
        category="evaluation",
    ),
    BiasDefinition(
        type="impact",
        name="Impact Bias",
        description="The tendency to overestimate the duration or the intensity of the impact of future feeling states.",
        examples=[
            "Overestimating how much winning the lottery will change your life",
            "Overestimating how devastating a layoff will be long-term",
        ],
        mitigation="Consider how others adapted to similar situations. Focus on process.",
        category="prediction",
    ),
    BiasDefinition(
        type="loss_aversion",
        name="Loss Aversion",
        description="The cognitive bias that causes people to strongly prefer avoiding losses over acquiring equivalent gains.",
        examples=[
            "Holding onto losing stocks too long to avoid realizing a loss",
            "Staying in an uncomfortable situation to avoid change",
        ],
        mitigation="Frame decisions in terms of opportunity costs. Consider expected value.",
        category="decision",
    ),
]
