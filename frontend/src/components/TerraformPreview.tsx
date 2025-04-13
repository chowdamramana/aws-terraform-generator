import * as React from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { TerraformOutput } from "@/types";
import Prism from "prismjs";
import "prismjs/themes/prism.css";

const TerraformPreview: React.FC = () => {
  const { configId } = useParams<{ configId: string }>();
  const { data, isLoading, error } = useQuery<TerraformOutput>({
    queryKey: ["terraform", configId],
    queryFn: async () => {
      const res = await api.get(`/preview/${configId}`);
      return res.data;
    },
    enabled: !!configId,
  });

  React.useEffect(() => {
    if (data?.code) {
      Prism.highlightAll();
    }
  }, [data]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading Terraform code</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl mb-4">Terraform Preview</h2>
      {data?.code ? (
        <>
          <pre className="language-hcl">
            <code>{data.code}</code>
          </pre>
          <Button
            onClick={() => navigator.clipboard.writeText(data.code)}
            className="mt-4"
          >
            Copy Code
          </Button>
        </>
      ) : (
        <p>No Terraform code available.</p>
      )}
    </div>
  );
};

export default TerraformPreview;