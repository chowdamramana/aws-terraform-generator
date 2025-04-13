export interface Module {
    name: string;
    version: string;
    url: string;
    description: string;
  }
  
  export interface ResourceConfig {
    id: string;
    type: string;
    properties: Record<string, any>;
  }
  
  export interface Config {
    id: string;
    name: string;
    resources: ResourceConfig[];
  }
  
  export interface TerraformOutput {
    code: string;
  }