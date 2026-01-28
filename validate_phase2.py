"""Quick validation: Run Phase 2.1 Video Generation Agent."""

import sys
from app.agents.video_generation.agent import VideoGenerationAgent
from app.agents.video_generation.models import VideoGenerationRequestInput, Platform

# Create agent
agent = VideoGenerationAgent()

# Create sample request (16 SBOX parameters)
request = VideoGenerationRequestInput(
    translation_id="sbox_validation_123",
    allocation_id="cim_validation_456",
    sbox_parameters={
        'cuts_per_30s': 8,
        'bpm_equivalent': 82,
        'tempo_curve': 'accelerating',
        'saturation': 0.379,
        'contrast': 'medium',
        'palette': 'vibrant',
        'framing': 'medium',
        'motion_style': 'dynamic',
        'focal_point': 'distributed',
        'voiceover_style': 'direct',
        'music_energy': 'driving',
        'voice_tone': 'friendly',
        'structure': 'observational',
        'cta_strength': 'medium',
        'proof_elements': 'moderate',
        'hook_placement': 'gradual'
    },
    platform=Platform.TIKTOK,
    duration=30
)

# Generate instruction
print("\n" + "="*80)
print("PHASE 2.1 VALIDATION: SBOX → Video Generation Instruction")
print("="*80)

try:
    instruction = agent.translate(request)
    
    print(f"\n✅ Instruction Generated: {instruction.instruction_id}")
    print(f"   Status: {instruction.status}")
    print(f"   Cost Estimate: ${instruction.estimated_cost}")
    print(f"   Generation Time: {instruction.estimated_generation_time}s")
    
    print(f"\n📝 MAIN PROMPT (for Runway):")
    print("-" * 80)
    print(instruction.main_prompt)
    
    print(f"\n🚫 NEGATIVE PROMPT:")
    print("-" * 80)
    print(instruction.negative_prompt)
    
    print(f"\n🎨 STYLE GUIDANCE:")
    print("-" * 80)
    print(instruction.style_guidance)
    
    print(f"\n📊 Agent Status:")
    status = agent.get_status()
    print(f"   Completed: {status.completed_instructions}")
    print(f"   Success Rate: {status.success_rate}%")
    print(f"   Uptime: {status.uptime_percentage}%")
    
    print("\n" + "="*80)
    print("✅ VALIDATION COMPLETE - Phase 2.1 Ready")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
