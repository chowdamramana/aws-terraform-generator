import * as React from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api, { fetchModules } from "@/lib/api";
import { Module, ResourceConfig } from "@/types";

const ResourceWizard: React.FC = () => {
  const navigate = useNavigate();
  const [module, setModule] = React.useState("");
  const [resourceType, setResourceType] = React.useState("");
  const [properties, setProperties] = React.useState<Record<string, string>>({});

  const { data: modules, isLoading: modulesLoading } = useQuery<Module[]>({
    queryKey: ["modules"],
    queryFn: fetchModules,
  });

  const createConfigMutation = useMutation({
    mutationFn: async (config: { name: string; resources: ResourceConfig[] }) => {
      const res = await api.post("/config", config);
      return res.data;
    },
    onSuccess: (data) => {
      navigate(`/preview/${data.id}`);
    },
  });

  if (modulesLoading) return <div>Loading modules...</div>;

  const handleModuleChange = (value: string) => {
    setModule(value);
    setResourceType("");
    setProperties({});
  };

  const handleTypeChange = (value: string) => {
    setResourceType(value);
    setProperties({});
  };

  const handlePropertyChange = (prop: string, value: string) => {
    setProperties((prev) => ({ ...prev, [prop]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const config = {
      name: `Config-${Date.now()}`,
      resources: [
        {
          id: `${module}-${resourceType}`,
          type: resourceType,
          properties,
        },
      ],
    };
    createConfigMutation.mutate(config);
  };

  const resourceTypes = module
    ? [
        { value: "aws_vpc", label: "VPC" },
        { value: "aws_s3_bucket", label: "S3 Bucket" },
      ]
    : [];

  return (
    <form onSubmit={handleSubmit} className="max-w-lg mx-auto p-4">
      <h2 className="text-2xl mb-4">Create Resource Configuration</h2>
      <div className="mb-4">
        <Label htmlFor="module">Module</Label>
        <Select
          options={modules?.map((m) => ({ value: m.name, label: m.name })) || []}
          value={module}
          onChange={handleModuleChange}
          placeholder="Select a module"
        />
      </div>
      {module && (
        <div className="mb-4">
          <Label htmlFor="resourceType">Resource Type</Label>
          <Select
            options={resourceTypes}
            value={resourceType}
            onChange={handleTypeChange}
            placeholder="Select resource type"
          />
        </div>
      )}
      {resourceType && (
        <>
          {Object.keys(properties).map((prop) => (
            <div key={prop} className="mb-4">
              <Label htmlFor={prop}>{prop}</Label>
              <Input
                id={prop}
                value={properties[prop]}
                onChange={(e) => handlePropertyChange(prop, e.target.value)}
              />
            </div>
          ))}
          <Button
            type="button"
            variant="outline"
            onClick={() =>
              handlePropertyChange(`prop${Object.keys(properties).length + 1}`, "")
            }
          >
            Add Property
          </Button>
        </>
      )}
      {resourceType && (
        <Button type="submit" className="mt-4">
          Create Config
        </Button>
      )}
    </form>
  );
};

export default ResourceWizard;