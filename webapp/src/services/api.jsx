import axios from "axios";

const baseURL = process.env.REACT_APP_API_BASE_URL;

const api = axios.create({
  baseURL,
});

const existingToken = localStorage.getItem("jwt_token");
if (existingToken) {
  api.defaults.headers.common["Authorization"] = `Bearer ${existingToken}`;
}

export const fetchAndStoreToken = async () => {
  try {
    const response = await axios.get(`${baseURL}/get_token`);
    const token = response.data.token;

    localStorage.setItem("jwt_token", token);
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    console.log("🔐 Token JWT armazenado.");
  } catch (error) {
    console.error("🚨 Erro ao buscar token JWT:", error);
  }
};

export const getMenuItems = async () => {
  try {
    const response = await api.get("/get_ml_execution_last_version");

    console.log("🔍 Resposta da API:", response.data);

    if (!Array.isArray(response.data)) {
      throw new Error("Resposta da API não é um array.");
    }

    return response.data.map(item => ({
      id: item.id,
      name: item.search || "Nome não disponível",
      date: item.date,
      version: item.version
    }));
  } catch (error) {
    console.error("🚨 Erro ao buscar itens do menu:", error);
    return [];
  }
};

export const runPipeline = async (payload) => {
  try {
    const response = await api.post("/run_pipeline", payload);
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao executar o pipeline:", error);
    throw error;
  }
};

export const getPipelineStatus = async (execId) => {
  try {
    const response = await api.get(`/get_pipeline_status?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao buscar status do pipeline:", error);
    return null;
  }
};

export const getAnalysesBySearch = async (searchTerm) => {
  try {
    const response = await api.get(`/get_ml_executions_by_search?search=${searchTerm}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching analyses:", error);
    return [];
  }
};

export const getSvmCategoryCounts = async (execId) => {
  try {
    const response = await api.get(`/get_svm_category_counts?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao buscar os dados do SVM:", error);
    return [];
  }
};

export const getWordCloud = async (execId) => {
  try {
    const response = await api.get(`/get_word_cloud?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao buscar dados da nuvem de palavras:", error);
    throw error;
  }
};

export const getCategoryColors = async (execId) => {
  try {
    const response = await api.get(`/get_category_colors?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Error fetching category colors:", error);
    return {};
  }
};

export const getModelsInfo = async () => {
  try {
    const response = await api.get("/get_models");

    return response.data;
  } catch (error) {
    console.error("🚨 Erro ao buscar modelos:", error);
    return {
      types: [],
      models: {}
    };
  }
};

export const deleteAnalysisByExecId = async (execId) => {
  try {
    const response = await api.delete(`/delete_execution?exec_id=${execId}`);
    return response.data;
  } catch (error) {
    console.error("🚨 Error deleting analysis:", error);
    throw error;
  }
};

export const getModelMetrics = async () => {
  try {
    const response = await api.get("/get_model_metrics");
    return response.data;
  } catch (error) {
    console.error("🚨 Error fetching model metrics:", error);
    return {};
  }
};

export const getSentencesByLabel = async (execId, label) => {
  const response = await api.get("/get_sentences_by_label", {
    params: { exec_id: execId, label },
  });
  return response.data;
};

export const getTimeSeriesLabel = async (execId) => {
  const response = await api.get("/get_time_series_label", {
    params: { exec_id: execId },
  });
  return response.data;
};

export default api;

