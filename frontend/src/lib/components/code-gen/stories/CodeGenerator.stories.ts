// 1. lib/components/code-gen/stories/CodeGenerator.stories.ts
import type { Meta, StoryObj } from '@storybook/svelte';
import CodeGenerator from '../CodeGenerator.svelte';

const meta = {
    title: 'CodeGen/CodeGenerator',
    component: CodeGenerator,
    tags: ['autodocs']
} satisfies Meta<CodeGenerator>;

export default meta;  // Add this line

type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    language: 'python',
    theme: 'dark'
  }
};