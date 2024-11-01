// lib/components/flow-builder/types.ts
interface NodePort {
  id: string;
  type: 'input' | 'output';
  name: string;
  schema: Record<string, unknown>;
}

interface NodeConfig {
  id: string;
  type: 'processor' | 'splitter';
  inputs: {
    params: NodePort;
    filters: NodePort;
    trigger: NodePort;
  };
  outputs: {
    success?: NodePort;
    failure?: NodePort;
    good?: NodePort;
    bad?: NodePort;
  };
  processing: {
    validation: Record<string, unknown>;
    transformation: Record<string, unknown>;
  };
}